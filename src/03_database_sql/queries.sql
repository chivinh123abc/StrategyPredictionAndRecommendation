-- ================================================================================
-- 5 CÂU TRUY VẤN SQL PHÂN TÍCH NÂNG CAO (ADVANCED SQL ANALYTICAL QUERIES)
-- Môn học: Nhập môn Khoa học Dữ liệu - PTIT (TS. Thái Tuyết Hải)
-- Giáo trình: Chương 5 & 5x (Databases, SQL & Pandas Manipulation)
-- CSDL: lol_live_data.db (3 bảng: matches_10min, tournament_matches, tournament_players)
-- ================================================================================

-- ================================================================================
-- TRUY VẤN 1: PHÂN TÍCH KÈO ĐẤU ĐỐI ĐẦU 1V1 (LANE MATCHUP ANALYSIS)
-- Kỹ thuật SQL: Self-JOIN (Ghép bảng chính nó qua gameid), GROUP BY, HAVING, WHERE.
-- Ý nghĩa nghiệp vụ: Thống kê đối đầu trực tiếp giữa 2 tướng ở cùng một vị trí 
-- (Đội Xanh vs Đội Đỏ) để phát hiện tướng khắc chế (Counter-Pick) và chênh lệch vàng/lính lúc 10 phút.
-- ================================================================================
-- !QUERY_1_START
SELECT 
    tp1.position AS lane,
    tp1.champion AS blue_champion,
    tp2.champion AS red_champion,
    COUNT(*) AS total_matches,
    SUM(tp1.result) AS blue_wins,
    ROUND(AVG(tp1.result) * 100.0, 1) AS blue_winrate_pct,
    ROUND(AVG(tp1.golddiffat10), 0) AS avg_blue_gold_diff_10,
    ROUND(AVG(tp1.csdiffat10), 1) AS avg_blue_cs_diff_10
FROM tournament_players tp1
JOIN tournament_players tp2 
    ON tp1.gameid = tp2.gameid 
   AND tp1.position = tp2.position 
   AND tp1.side = 'Blue' 
   AND tp2.side = 'Red'
WHERE tp1.position IN ('top', 'mid', 'bot')
GROUP BY tp1.position, tp1.champion, tp2.champion
HAVING total_matches >= 5
ORDER BY total_matches DESC, blue_winrate_pct DESC;
-- !QUERY_1_END


-- ================================================================================
-- TRUY VẤN 2: PHÂN TÍCH CẶP ĐÔI ĂN Ý ĐƯỜNG DƯỚI (BOT LANE SYNERGY DUO)
-- Kỹ thuật SQL: Intra-team JOIN (Ghép 2 tuyển thủ cùng team), GROUP BY, HAVING count(*) >= 10.
-- Ý nghĩa nghiệp vụ: Tìm kiếm các tổ hợp Xạ thủ (Bot) + Hỗ trợ (Sup) có tỷ lệ thắng cao nhất,
-- phục vụ thuật toán gợi ý Synergy trong hệ thống Ban/Pick Recommender (Chương 6).
-- ================================================================================
-- !QUERY_2_START
SELECT 
    p1.champion AS adc_champion,
    p2.champion AS support_champion,
    COUNT(*) AS duo_matches,
    SUM(p1.result) AS duo_wins,
    ROUND(AVG(p1.result) * 100.0, 1) AS duo_winrate_pct,
    ROUND(AVG(p1.goldat10 + p2.goldat10), 0) AS avg_duo_gold_10,
    ROUND(AVG(p1.kills + p2.kills), 1) AS avg_duo_kills,
    ROUND(AVG(p1.deaths + p2.deaths), 1) AS avg_duo_deaths
FROM tournament_players p1
JOIN tournament_players p2 
    ON p1.gameid = p2.gameid 
   AND p1.side = p2.side 
   AND p1.position = 'bot' 
   AND p2.position = 'sup'
GROUP BY p1.champion, p2.champion
HAVING duo_matches >= 10
ORDER BY duo_winrate_pct DESC, duo_matches DESC;
-- !QUERY_2_END


-- ================================================================================
-- TRUY VẤN 3: TƯỚNG CÓ TỶ LỆ CẤM/CHỌN CAO NHẤT (META PRESENCE RATE)
-- Kỹ thuật SQL: Common Table Expressions (CTE / Subqueries), Unpivot UNION ALL, JOIN.
-- Ý nghĩa nghiệp vụ: Xác định các vị tướng định hình Meta của mùa giải qua chỉ số
-- Presence Rate = (Lượt Chọn + Lượt Cấm) / Tổng số trận đấu.
-- ================================================================================
-- !QUERY_3_START
WITH TotalMatches AS (
    SELECT COUNT(DISTINCT gameid) AS total_games FROM tournament_matches
),
Picks AS (
    SELECT champion, COUNT(*) AS pick_count
    FROM tournament_players
    WHERE champion IS NOT NULL
    GROUP BY champion
),
Bans AS (
    SELECT ban_champion, COUNT(*) AS ban_count
    FROM (
        SELECT ban1 AS ban_champion FROM tournament_matches WHERE ban1 IS NOT NULL AND ban1 != 'NoBan'
        UNION ALL SELECT ban2 FROM tournament_matches WHERE ban2 IS NOT NULL AND ban2 != 'NoBan'
        UNION ALL SELECT ban3 FROM tournament_matches WHERE ban3 IS NOT NULL AND ban3 != 'NoBan'
        UNION ALL SELECT ban4 FROM tournament_matches WHERE ban4 IS NOT NULL AND ban4 != 'NoBan'
        UNION ALL SELECT ban5 FROM tournament_matches WHERE ban5 IS NOT NULL AND ban5 != 'NoBan'
    )
    GROUP BY ban_champion
),
Winrates AS (
    SELECT champion, SUM(result) AS wins, ROUND(AVG(result) * 100.0, 1) AS winrate_pct
    FROM tournament_players
    WHERE champion IS NOT NULL
    GROUP BY champion
)
SELECT 
    COALESCE(p.champion, b.ban_champion) AS champion,
    COALESCE(p.pick_count, 0) AS picks,
    COALESCE(b.ban_count, 0) AS bans,
    COALESCE(p.pick_count, 0) + COALESCE(b.ban_count, 0) AS total_presence,
    ROUND((COALESCE(p.pick_count, 0) + COALESCE(b.ban_count, 0)) * 100.0 / (SELECT total_games FROM TotalMatches), 2) AS presence_pct,
    COALESCE(w.winrate_pct, 0.0) AS winrate_pct
FROM Picks p
FULL OUTER JOIN Bans b ON p.champion = b.ban_champion
LEFT JOIN Winrates w ON COALESCE(p.champion, b.ban_champion) = w.champion
ORDER BY total_presence DESC
LIMIT 20;
-- !QUERY_3_END


-- ================================================================================
-- TRUY VẤN 4: XẾP HẠNG TUYỂN THỦ LẤN ĐƯỜNG PHÚT 10 (LANE DOMINANCE RANKING)
-- Kỹ thuật SQL: Window Functions (DENSE_RANK(), PARTITION BY, AVG() OVER()).
-- Ý nghĩa nghiệp vụ: Xếp hạng khả năng đè đường lúc 10 phút của các tuyển thủ theo từng lane
-- và so sánh với mức chuẩn trung bình (Benchmark) của toàn bộ giải đấu ở vị trí đó.
-- ================================================================================
-- !QUERY_4_START
WITH PlayerAggregates AS (
    SELECT 
        playername,
        position,
        teamname,
        league,
        COUNT(*) AS games_played,
        ROUND(AVG(golddiffat10), 0) AS avg_gold_diff_10,
        ROUND(AVG(csdiffat10), 1) AS avg_cs_diff_10,
        ROUND(AVG(result) * 100.0, 1) AS winrate_pct
    FROM tournament_players
    WHERE playername IS NOT NULL AND playername != 'Unknown'
    GROUP BY playername, position, teamname, league
    HAVING games_played >= 15
),
RankedPlayers AS (
    SELECT 
        playername,
        position,
        teamname,
        league,
        games_played,
        avg_gold_diff_10,
        avg_cs_diff_10,
        winrate_pct,
        DENSE_RANK() OVER (PARTITION BY position ORDER BY avg_gold_diff_10 DESC) AS lane_gold_rank,
        ROUND(AVG(avg_gold_diff_10) OVER (PARTITION BY position), 0) AS position_benchmark_gold_diff
    FROM PlayerAggregates
)
SELECT * FROM RankedPlayers
WHERE lane_gold_rank <= 3
ORDER BY position, lane_gold_rank;
-- !QUERY_4_END


-- ================================================================================
-- TRUY VẤN 5: ĐỐI CHIẾU HIỆU QUẢ LĂN CẦU TUYẾT: ĐẤU GIẢI VS RANK ĐƠN (SNOWBALL COMPARISON)
-- Kỹ thuật SQL: UNION ALL, CASE WHEN (Phân tầng rời rạc hóa), GROUP BY, Aggregate functions.
-- Ý nghĩa nghiệp vụ: So sánh khả năng chuyển hóa lợi thế vàng lúc 10 phút thành chiến thắng 
-- giữa môi trường thi đấu chuyên nghiệp (Pro Play) và môi trường Rank Thách Đấu Solo Queue.
-- ================================================================================
-- !QUERY_5_START
WITH ProPlayLead AS (
    SELECT 
        '1. Đấu Giải (Oracle Esports)' AS dataset_type,
        CASE 
            WHEN golddiffat10 >= 2000 THEN '1. Dẫn Lớn (>= +2000g)'
            WHEN golddiffat10 >= 1000 THEN '2. Dẫn Vừa (+1000g đến +1999g)'
            WHEN golddiffat10 >= -999 AND golddiffat10 <= 999 THEN '3. Cân Bằng (-999g đến +999g)'
            WHEN golddiffat10 >= -1999 THEN '4. Thua Vừa (-1000g đến -1999g)'
            ELSE '5. Thua Sâu (<= -2000g)'
        END AS gold_diff_tier,
        COUNT(*) AS total_matches,
        SUM(result) AS wins,
        ROUND(AVG(result) * 100.0, 2) AS winrate_pct,
        ROUND(AVG(gamelength) / 60.0, 1) AS avg_duration_min
    FROM tournament_matches
    WHERE datacompleteness = 'complete'
    GROUP BY gold_diff_tier
),
SoloRankLead AS (
    SELECT 
        '2. Solo Rank (Riot API)' AS dataset_type,
        CASE 
            WHEN blueGoldDiff >= 2000 THEN '1. Dẫn Lớn (>= +2000g)'
            WHEN blueGoldDiff >= 1000 THEN '2. Dẫn Vừa (+1000g đến +1999g)'
            WHEN blueGoldDiff >= -999 AND blueGoldDiff <= 999 THEN '3. Cân Bằng (-999g đến +999g)'
            WHEN blueGoldDiff >= -1999 THEN '4. Thua Vừa (-1000g đến -1999g)'
            ELSE '5. Thua Sâu (<= -2000g)'
        END AS gold_diff_tier,
        COUNT(*) AS total_matches,
        SUM(blueWins) AS wins,
        ROUND(AVG(blueWins) * 100.0, 2) AS winrate_pct,
        ROUND(AVG(gameDuration) / 60.0, 1) AS avg_duration_min
    FROM matches_10min
    GROUP BY gold_diff_tier
)
SELECT * FROM ProPlayLead
UNION ALL
SELECT * FROM SoloRankLead
ORDER BY dataset_type, gold_diff_tier;
-- !QUERY_5_END
