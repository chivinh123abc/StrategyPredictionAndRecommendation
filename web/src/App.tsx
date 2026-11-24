import { useEffect, useMemo, useRef, useState } from 'react'
import type { DragEvent } from 'react'
import { request } from './api'
import type { Candidate, Catalog, Champion, Explanation, GameInput, Role, Session, Settings, Side, SourceComparison, SourceStats, View } from './types'

const ROLES: Role[] = ['top', 'jng', 'mid', 'bot', 'sup']
const ROLE: Record<Role, string> = { top: 'Top', jng: 'Rừng', mid: 'Mid', bot: 'Xạ thủ', sup: 'Hỗ trợ' }
const STORAGE = 'draft-lab-session-v1'
const initial = (): Session => ({ settings: { region: 'WLDS', blue_team: 'T1', red_team: 'Gen.G', ban_strategy: 'contextual', as_of: null, allow_statistical_auto: false }, completed: [], current: { first_side: 'blue', history: [], swaps: [] } })
function saved(): Session {
  try { const data = JSON.parse(localStorage.getItem(STORAGE) || 'null'); if (data?.version === 1 && Array.isArray(data.session?.current?.history) && Array.isArray(data.session?.completed) && typeof data.session?.settings?.blue_team === 'string' && typeof data.session?.settings?.red_team === 'string' && ['blue', 'red'].includes(data.session.current.first_side)) return data.session } catch { /* A new draft remains available if browser storage is unavailable. */ }
  return initial()
}
const points = (row: Candidate) => (row.ranking_score ?? row.priority_pct ?? 0).toLocaleString('vi-VN', { maximumFractionDigits: 2 })
const percent = (n: number | null | undefined) => n == null ? '—' : `${(n * 100).toFixed(1)}%`
const signed = (n: unknown) => typeof n !== 'number' ? '—' : `${n > 0 ? '+' : ''}${Math.round(n).toLocaleString('vi-VN')}`
const date = (value: string) => new Date(value).toLocaleDateString('vi-VN')
function laneSummary(row: Candidate) {
  const lane = row.lane_review
  if (!lane?.opponent) return null
  const pro = row.matchup_source_comparison?.find(p => p.role === row.role && p.opponent === lane.opponent)?.pro
  return `Kèo ${lane.opponent}: n=${lane.games} · WR trận ${percent(lane.winrate)} · Cận dưới 95% ${percent(lane.ranking_confidence_bound)}${pro ? ` · GD15 ${signed(pro.gold_diff_15_mean)} (n=${pro.gold_diff_15_n ?? 0})` : ''}`
}
function list(value: string | undefined): string { try { return JSON.parse(value || '[]').join(', ') || 'Chưa có mẫu' } catch { return 'Chưa rõ' } }

function Portrait({ name, lookup, small = false }: { name?: string; lookup: Map<string, Champion>; small?: boolean }) {
  const champion = name ? lookup.get(name) : undefined
  return <span className={`portrait ${small ? 'small' : ''}`}><span aria-hidden="true">{champion?.label.slice(0, 2).toUpperCase() || '—'}</span>{champion && <img src={champion.image} alt="" draggable={false} loading="lazy" onError={event => { event.currentTarget.style.display = 'none' }} />}</span>
}

function SourceTable({ row }: { row: SourceComparison }) {
  const labels: Record<string, string> = { opposite_supported_intervals: 'Hai nguồn cho khoảng lợi thế trái chiều.', opposite_means_uncertain: 'Trung bình trái chiều, nhưng còn bất định.', insufficient_measurements: 'Chưa đủ số đo để so sánh lợi thế.', no_observed_direction_conflict: 'Chưa thấy trung bình trái chiều.' }
  const metrics = [['gold_diff_10', 'Chênh vàng · 10′'], ['gold_diff_15', 'Chênh vàng · 15′'], ['xp_diff_10', 'Chênh XP · 10′'], ['xp_diff_15', 'Chênh XP · 15′'], ['cs_diff_10', 'Chênh CS · 10′'], ['cs_diff_15', 'Chênh CS · 15′']]
  function uncertainty(source: SourceStats, key: string) { return `${signed(source[`${key}_mean_ci95_low`])} … ${signed(source[`${key}_mean_ci95_high`])}` }
  return <section className="source-block" data-testid="source-comparison">
    <div className="section-line"><strong>Gặp {row.opponent}</strong><span>p(vị trí) {row.enemy_role_probability.toFixed(2)}</span></div>
    <table className="source-table"><thead><tr><th>Chỉ số</th><th>Pro</th><th>Rank</th></tr></thead><tbody>
      <tr><td>Số trận</td><td>{row.pro.games}</td><td>{row.rank.games}</td></tr>
      <tr><td>Thắng cả trận</td>{[row.pro, row.rank].map((source, i) => <td key={i}>{percent(source.winrate)}<small>CI95 {percent(source.ci95_wilson[0])}–{percent(source.ci95_wilson[1])}</small></td>)}</tr>
      {metrics.map(([key, label]) => <tr key={key}><td>{label}</td>{[row.pro, row.rank].map((source, i) => <td key={i}>{signed(source[`${key}_mean`])}<small>n={String(source[`${key}_n`] ?? 0)} · CI {uncertainty(source, key)}</small></td>)}</tr>)}
    </tbody></table>
    <p className="evidence-note">{labels[row.comparison.gd15_comparison] || 'Hai nguồn chưa đủ bằng chứng.'} {row.comparison.sample_status === 'insufficient_samples' && 'Có nguồn dưới 5 mẫu.'}</p>
    <details><summary>Nguồn và thời điểm</summary><p>Pro: {list(row.pro.platforms)} · patch {list(row.pro.patches)}</p><p>Rank: {list(row.rank.platforms)} · patch {list(row.rank.patches)}</p><p>Rank được chụp cho phiên lúc {new Date(row.rank_frozen_at).toLocaleString('vi-VN')}. Đây là rank tại lúc kiểm tra, không xác nhận rank lịch sử chính xác.</p></details>
  </section>
}

function Inspector({ advice, title, notice, onClose }: { advice: Candidate | null; title: string; notice?: string | null; onClose: () => void }) {
  const [collapsed, setCollapsed] = useState(false)
  return <aside className="panel inspector" aria-label="Bằng chứng gợi ý">
    <div className="panel-heading"><button className="quiet inspector-collapse" aria-expanded={!collapsed} aria-controls="inspector-body" onClick={() => setCollapsed(value => !value)}><span className="eyebrow">HIỂU LỰA CHỌN</span><span>{collapsed ? `▸ Mở rộng · ${title}` : '▾ Thu gọn toàn bộ'}</span></button><button className="quiet" onClick={onClose} aria-label="Đóng hiểu lựa chọn">Đóng ×</button></div>
    {!collapsed && <div id="inspector-body">
    <h2>{title}</h2>
    {!advice ? <p className="empty-copy">{notice || 'Chọn một gợi ý để xem lý do và số mẫu. Bạn cũng có thể bấm vào một lượt trong lịch sử.'}</p> : <>
      {advice.review_required && <div className="warning">Thiếu bằng chứng đối đầu đủ mẫu. Lựa chọn này chưa được xác nhận là counter.</div>}
      {advice.lane_review?.requires_review && <div className="warning" data-testid="lane-review"><strong>Kèo cùng đường chưa đủ căn cứ</strong><p>{advice.lane_review.reason}</p><p>Chỉ xác nhận tay hoặc bật chế độ test mới chấp nhận lựa chọn này.</p></div>}
      {advice.lane_review?.opponent && <p className="micro">Cận dưới CI95 của WR cả trận: {percent(advice.lane_review.ranking_confidence_bound)} (tham khảo). Kèo dưới 5 mẫu không được dùng Wilson để đảo thứ tự điểm tổng; vẫn cần xem lại trước khi tự chốt.</p>}
      {advice.pair_reservation?.reason && <div className={advice.pair_reservation.status === 'secure_now' ? 'pair-safe-note' : 'warning'}><strong>{advice.pair_reservation.status === 'secure_now' ? 'Ưu tiên giữ cặp bot' : 'Kiểm tra cặp bot'}</strong><p>{advice.pair_reservation.reason}</p>{advice.pair_reservation.supported_partners && <p>Đối tác đủ mẫu: {advice.pair_reservation.supported_partners.map(p => `${p.champion} (n=${p.games})`).join(', ') || 'Chưa có'}</p>}{advice.pair_reservation.pair_evidence && <p>n={advice.pair_reservation.pair_evidence.games} · WR cả trận {percent(advice.pair_reservation.pair_evidence.winrate)} · CI95 {advice.pair_reservation.pair_evidence.ci95_wilson.map(percent).join('–')}</p>}</div>}
      {advice.historical && <div className="fact-grid"><div><span>Lịch sử tướng / role</span><strong>{advice.historical.games}<small> trận</small></strong></div><div><span>Thắng cả trận</span><strong>{percent(advice.historical.winrate)}</strong></div></div>}
      <div className="reason-list">{(advice.reasons || (advice.reason ? [advice.reason] : [])).slice(0, 3).map((reason, i) => <p key={i}>{reason}</p>)}</div>
      {advice.score_components && <details><summary>Thành phần điểm</summary><div className="components">{Object.entries(advice.score_components).map(([key, part]) => <div key={key}><span>{key}</span><b>{part.value.toFixed(3)} <small>× {part.weight}</small></b></div>)}</div><p>Điểm ưu tiên, không phải xác suất thắng. Vàng/XP/CS đầu trận hiện dùng để giải thích, chưa cộng vào điểm gốc. Kèo đã lộ được kiểm tra số mẫu riêng. Nhóm cùng mức bằng chứng xếp theo điểm gốc; Wilson của kèo ít mẫu chỉ để tham khảo.</p></details>}
      {(advice.matchup_source_comparison || []).map(row => <SourceTable key={`${row.role}:${row.opponent}`} row={row} />)}
      {!advice.matchup_source_comparison?.length && <p className="empty-copy">{advice.historical ? 'Chưa có đối thủ cùng vị trí được hỗ trợ để hiển thị bảng Pro / Rank.' : 'Gợi ý ban dựa trên lịch sử và pool lựa chọn. Không có tỷ lệ thắng được gán cho lượt ban.'}</p>}
    </>}
    <p className="inspector-foot">Quan sát lịch sử không chứng minh khắc chế cơ chế hay mức tăng thắng. “—” là thiếu dữ liệu.</p>
    </div>}
  </aside>
}

export default function App() {
  const [session, setSession] = useState<Session>(saved)
  const [catalog, setCatalog] = useState<Catalog | null>(null)
  const [view, setView] = useState<View | null>(null)
  const [busy, setBusy] = useState(true)
  const [error, setError] = useState('')
  const [retry, setRetry] = useState(0)
  const [selected, setSelected] = useState<Candidate | null>(null)
  const [inspection, setInspection] = useState<Explanation | null>(null)
  const [inspectorOpen, setInspectorOpen] = useState(false)
  const [onlyRole, setOnlyRole] = useState<Role | null>(null)
  const [manual, setManual] = useState(false)
  const [search, setSearch] = useState('')
  const [manualName, setManualName] = useState('')
  const [dragging, setDragging] = useState<{side: Side; champion: string} | null>(null)
  const [displayIndex, setDisplayIndex] = useState(session.completed.length)
  const [automating, setAutomating] = useState(false)
  const [nextFirstSide, setNextFirstSide] = useState<Side | ''>('')
  const autoRef = useRef(false)
  const generation = useRef(0)
  const lookup = useMemo(() => new Map(catalog?.champions.map(champion => [champion.name, champion]) || []), [catalog])
  const label = (name: string) => lookup.get(name)?.label || name
  const activeIndex = session.completed.length
  const archive = displayIndex !== activeIndex
  const game = view?.games[displayIndex]
  const turn = archive ? null : view?.turn
  const names = { blue: session.settings.blue_team, red: session.settings.red_team }
  const teams = catalog?.regions.find(r => r.code === session.settings.region)?.teams || []
  const lockedSettings = session.current.history.length > 0 || session.completed.length > 0
  const unavailable = new Set(game ? [...game.used_champions, ...game.bans.blue, ...game.bans.red, ...Object.values(game.picks.blue), ...Object.values(game.picks.red)] : [])
  const manualPlacement = view?.role_preferences?.[manualName]?.find(p => turn && !game?.picks[turn.side][p.role])
  const manualRole = manualPlacement?.role

  function accept(next: View) {
    setView(next); setSession(next.session); setOnlyRole(next.only_role); setDisplayIndex(next.session.completed.length)
    setSelected(null); setInspection(null); setInspectorOpen(false); setManual(false); setManualName(''); setSearch(''); setDragging(null); setError('')
    setNextFirstSide('')
    try { localStorage.setItem(STORAGE, JSON.stringify({ version: 1, session: next.session })) } catch { /* Export remains available. */ }
  }

  useEffect(() => {
    const controller = new AbortController(); const id = ++generation.current
    setBusy(true)
    Promise.all([request<Catalog>('/catalog', undefined, controller.signal).then(data => { if (id === generation.current) setCatalog(data); return data }), request<View>('/draft/view', { session }, controller.signal)])
      .then(([data, draft]) => { if (id === generation.current) { setCatalog(data); accept(draft) } })
      .catch(reason => { if (!controller.signal.aborted) setError(reason instanceof TypeError ? 'Chưa kết nối được phần xử lý. Kiểm tra cửa sổ chạy ứng dụng rồi thử lại.' : reason.message) })
      .finally(() => { if (id === generation.current) setBusy(false) })
    return () => controller.abort()
    // Session changes are submitted explicitly, so a move is never sent twice by an effect.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [retry])

  async function submit(path: string, next = session, extra: Record<string, unknown> = {}, role = onlyRole) {
    const id = ++generation.current; setBusy(true); setError('')
    try { const result = await request<View>(path, { session: next, only_role: role, ...extra }); if (id === generation.current) accept(result) }
    catch (reason) { if (id === generation.current) { setSession(view?.session || session); setError(reason instanceof Error ? reason.message : 'Không thể thực hiện thao tác.') } }
    finally { if (id === generation.current) setBusy(false) }
  }

  function setting<K extends keyof Settings>(key: K, value: Settings[K]) {
    const next = { ...session, settings: { ...session.settings, [key]: value } }
    if (key !== 'allow_statistical_auto') next.snapshot_id = null
    if (key === 'region') {
      const available = catalog?.regions.find(r => r.code === value)?.teams || []
      next.settings.blue_team = available.includes(next.settings.blue_team) ? next.settings.blue_team : available[0]
      next.settings.red_team = available.includes(next.settings.red_team) && next.settings.red_team !== next.settings.blue_team ? next.settings.red_team : available.find(t => t !== next.settings.blue_team) || available[0]
    }
    if (key === 'allow_statistical_auto') setSession(next)
    void submit('/draft/view', next)
  }

  async function autoGame() {
    autoRef.current = true; setAutomating(true); setBusy(true); setError(''); let next = session
    try {
      for (let i = 0; i < 20 && autoRef.current; i++) {
        const result = await request<View>('/draft/action', { session: next, only_role: null, auto: true })
        accept(result); next = result.session
        if (!result.turn) break
        await new Promise(resolve => setTimeout(resolve, 90))
      }
    } catch (reason) { setError(reason instanceof Error ? reason.message : 'Tự draft đã dừng.') }
    finally { autoRef.current = false; setAutomating(false); setBusy(false) }
  }

  async function inspectTurn(index: number) {
    if (inspection?.move.turn === index && inspectorOpen) { setInspection(null); setInspectorOpen(false); return }
    setBusy(true); setError('')
    try { setInspection(await request<Explanation>('/draft/explain', { session, game_index: displayIndex, turn: index })); setInspectorOpen(true) }
    catch (reason) { setError(reason instanceof Error ? reason.message : 'Không đọc được bằng chứng.') }
    finally { setBusy(false) }
  }

  function undo() {
    const history = session.current.history.slice(0, -1)
    void submit('/draft/view', { ...session, current: { ...session.current, history, swaps: session.current.swaps.filter(s => s.after_turn <= history.length) } })
  }

  function nextGame() {
    if (!nextFirstSide) return
    const next: GameInput = { first_side: nextFirstSide, history: [], swaps: [] }
    void submit('/draft/view', { ...session, completed: [...session.completed, session.current], current: next }, {}, null)
  }

  function dropChampion(event: DragEvent<HTMLDivElement>, side: Side, target_role: Role) {
    event.preventDefault()
    if (busy || archive) return
    try {
      const source = JSON.parse(event.dataTransfer.getData('application/x-draft-slot')) as {side: Side; champion: string}
      setDragging(null)
      if (source.side !== side) { setError('Chỉ đổi vị trí tướng trong cùng một đội.'); return }
      if (game?.picks[side][target_role] === source.champion) return
      void submit('/draft/swap', session, {side, champion: source.champion, target_role})
    } catch { setDragging(null) }
  }

  function download() {
    const file = new Blob([JSON.stringify({ version: 1, session, scope: view?.scope, configuration: view?.configuration, boards: view?.games, interpretation: 'Draft demo; no game results or causal win uplift.' }, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(file); const anchor = document.createElement('a'); anchor.href = url; anchor.download = 'draft-lab-bo5.json'; anchor.click(); URL.revokeObjectURL(url)
  }

  return <div className="app">
    <header className="topbar">
      <a className="brand" href="#"><svg width="28" height="32" viewBox="0 0 28 32" aria-hidden="true"><path d="M3 3h19v16L12 29 3 20V3Z" fill="none" stroke="currentColor" strokeWidth="2" /><path d="M9 9h8v8l-4 4-4-4V9Z" fill="currentColor" /></svg><span>DRAFT<span className="brand-light">LAB</span><small>BAN / PICK WORKSPACE</small></span></a>
      <div className="header-note">Đấu giải <span className="dot">·</span> Bản chụp lịch sử</div>
      <div className="header-actions"><button className="quiet" onClick={download}>↓ Xuất JSON</button><button className="outline" onClick={() => { setManual(false); void submit('/draft/view', initial(), {}, null) }} disabled={busy}>↻ Phiên mới</button></div>
    </header>

    <div className="page-title"><div><span className="eyebrow">PHÒNG TẬP CHIẾN THUẬT</span><h1>Mỗi lượt chọn, một căn cứ.</h1><p>Chuẩn bị draft cùng dữ liệu lịch sử, theo dõi cả chuỗi Fearless.</p></div>{view && <div className="data-stamp"><span className="status-dot" />{view.scope.region} <b>PATCH {view.scope.dataset_patch}</b><small>Dữ liệu đến {date(view.scope.data_through)} · {view.scope.history_games} trận trong cửa sổ</small></div>}</div>
    {view && <div className="configuration-strip" data-testid="configuration">Ban: <b>{view.configuration.ban_strategy}</b> · Pick: <b>{view.configuration.pick_scoring}{view.configuration.pair_safety ? ' + giữ cặp bot' : ''}{view.configuration.lane_review_policy ? ' + kiểm kèo' : ''}</b> · Mốc cố định: <b>{session.settings.as_of}</b> · Phiên dữ liệu <code title={view.configuration.snapshot_id}>{view.configuration.snapshot_id.slice(0, 12)}</code><small>Contextual v2 · Điểm ưu tiên, không phải xác suất thắng</small></div>}
    {error && <div className="error-banner" role="alert"><span>{error}</span>{!view && <button onClick={() => setRetry(n => n + 1)} disabled={busy}>Thử lại</button>}</div>}

    <div className="workspace">
      <aside className="setup panel">
        <div className="setup-header"><div><span className="eyebrow">THIẾT LẬP PHIÊN</span><h2>Draft của bạn</h2></div>
          <div className="series-navigation"><span className="micro">FEARLESS BO5 · Ván {activeIndex + 1}</span><div className="game-tabs" aria-label="Các ván draft">{Array.from({ length: 5 }, (_, index) => <button key={index} className={displayIndex === index ? 'active' : ''} disabled={index > activeIndex || busy} onClick={() => { setDisplayIndex(index); setInspection(null); setInspectorOpen(false); setSelected(null); setManualName('') }}>{index + 1}{view?.games[index]?.complete && <small>✓</small>}</button>)}</div></div>
          {view && !view.turn && !view.series_complete && <div className="next-game-choice"><label>Chọn trước ván {activeIndex + 2}<select aria-label="Đội chọn trước ván tiếp theo" value={nextFirstSide} disabled={busy} onChange={e => setNextFirstSide(e.target.value as Side | '')}><option value="">Chọn đội…</option><option value="blue">{names.blue} · Blue</option><option value="red">{names.red} · Red</option></select></label><button className="primary" onClick={nextGame} disabled={busy || !nextFirstSide}>Sang ván {activeIndex + 2} →</button></div>}
        </div>
        <div className="setup-fields">
        <label>Giải / khu vực<select value={session.settings.region} disabled={busy || lockedSettings} onChange={e => setting('region', e.target.value as Settings['region'])}>{(catalog?.regions || [{ code: 'WLDS', teams: [], games: 0 }]).map(r => <option key={r.code} value={r.code}>{r.code === 'WLDS' ? 'Worlds · WLDS' : r.code}</option>)}</select></label>
        <label>Đội xanh<select aria-label="Đội xanh" value={session.settings.blue_team} disabled={busy || lockedSettings} onChange={e => setting('blue_team', e.target.value)}>{teams.map(t => <option key={t} disabled={t === session.settings.red_team}>{t}</option>)}</select></label>
        <label>Đội đỏ<select aria-label="Đội đỏ" value={session.settings.red_team} disabled={busy || lockedSettings} onChange={e => setting('red_team', e.target.value)}>{teams.map(t => <option key={t} disabled={t === session.settings.blue_team}>{t}</option>)}</select></label>
        <label>Đội chọn trước<select aria-label="Đội chọn trước" value={session.current.first_side} disabled={busy || session.current.history.length > 0} onChange={e => void submit('/draft/view', { ...session, current: { ...session.current, first_side: e.target.value as Side } })}><option value="blue">{names.blue} · Xanh</option><option value="red">{names.red} · Đỏ</option></select></label>
        <label>Cách gợi ý ban<select value={session.settings.ban_strategy} disabled={busy || lockedSettings} onChange={e => setting('ban_strategy', e.target.value as Settings['ban_strategy'])}><option value="contextual">Contextual · Theo ngữ cảnh</option><option value="legacy">Legacy · Theo lịch sử</option></select></label>
        <label>Mốc dữ liệu lịch sử<input type="date" value={session.settings.as_of || ''} disabled={busy || lockedSettings} onChange={e => setting('as_of', e.target.value || null)} /></label>
        </div>
        <div className="setup-footer">
        <p className="micro">Blue/Red chọn trước theo từng ván, có thể cùng bên suốt BO5. Không tự luân phiên.</p>
        <p className="muted">{game?.used_champions.length || 0} tướng bị khóa từ các ván trước. Ban thường được đặt lại mỗi ván.</p>
        {game && game.used_champions.length > 0 && <details><summary>Xem tướng đã dùng</summary><div className="locked-list">{game.used_champions.map(c => <span key={c}>{label(c)}</span>)}</div></details>}
        <label className="checkbox"><input type="checkbox" checked={session.settings.allow_statistical_auto} disabled={busy} onChange={e => setting('allow_statistical_auto', e.target.checked)} /><span>Cho phép chọn thiếu bằng chứng <small>(chỉ test)</small></span></label>
        </div>
      </aside>

      <main className="draft-main">
        <section className="turn-bar" aria-live="polite" data-testid="current-turn"><div><span className="eyebrow">{archive ? `ĐANG XEM VÁN ${displayIndex + 1}` : `VÁN ${activeIndex + 1} / 5`}</span><h2>{archive ? 'Lịch sử draft' : turn ? <><span className={`side-dot ${turn.side}`} />{names[turn.side]} <span className="turn-kind">{turn.action === 'ban' ? 'cấm' : 'chọn'} {turn.number}</span></> : view ? 'Đã hoàn tất draft' : 'Đang nạp lịch sử…'}</h2></div><div className="turn-counter">{game?.history.length || 0}<span>/20 lượt</span></div></section>
        <div className="teams-grid">{(['blue', 'red'] as Side[]).map(side => <section key={side} className={`team-panel ${side} ${turn?.side === side ? 'acting' : ''}`} aria-label={`Bảng đội ${side === 'blue' ? 'xanh' : 'đỏ'}`}>
          <div className="team-heading"><span>{side === 'blue' ? 'BLUE SIDE' : 'RED SIDE'}</span><strong>{names[side]}</strong>{turn?.side === side && <span className="turn-chip">Đến lượt</span>}</div>
          <div className="ban-slots">{Array.from({ length: 5 }, (_, index) => { const champion = game?.bans[side][index]; return <div key={index} className={`ban-slot ${index === 3 ? 'phase-two' : ''} ${turn?.action === 'ban' && turn.side === side && turn.number === index + 1 ? 'next' : ''}`} title={champion ? label(champion) : `Ban ${index + 1}`}><Portrait name={champion} lookup={lookup} small /><span>B{index + 1}</span></div> })}</div>
          <div className="role-slots">{ROLES.map(role => { const champion = game?.picks[side][role]; return <div data-testid={`slot-${side}-${role}`} className={`role-slot ${champion ? 'filled' : ''} ${dragging?.side === side ? 'drop-zone' : ''}`} key={role} draggable={!!champion && !busy && !archive} onDragStart={event => { if (!champion) return; setDragging({side,champion}); event.dataTransfer.setData('application/x-draft-slot', JSON.stringify({side,champion})); event.dataTransfer.effectAllowed='move' }} onDragEnd={() => setDragging(null)} onDragOver={event => { if (!busy && !archive) { event.preventDefault(); event.dataTransfer.dropEffect='move' } }} onDrop={event => dropChampion(event,side,role)}><span className="role-glyph" title={ROLE[role]}>{role === 'jng' ? 'J' : role.slice(0, 1).toUpperCase()}</span><Portrait name={champion} lookup={lookup} /><div className="slot-copy"><span>{ROLE[role]}</span><strong>{champion ? label(champion) : 'Chưa chọn'}</strong><small>{view?.rosters[side]?.[role] || 'Chưa có hồ sơ tuyển thủ'}</small></div>{champion && <select className="swap-select" aria-label={`Đổi vị trí ${label(champion)}`} value={role} disabled={busy || archive} onChange={e => void submit('/draft/swap', session, { side, champion, target_role: e.target.value })}>{ROLES.map(r => <option key={r} value={r}>{ROLE[r]}</option>)}</select>}</div> })}</div>
          <div className="team-footer">{Object.keys(game?.picks[side] || {}).length}/5 vị trí <span>Kéo thả tướng để đổi đường · Menu hỗ trợ bàn phím/chạm</span></div>
        </section>)}</div>

        <section className={`panel recommendations ${archive || !turn ? 'no-manual' : ''}`} aria-label="Gợi ý từ hệ thống"><div className="recommend-heading"><div><span className="eyebrow">LỰA CHỌN THAM KHẢO</span><h2>{archive ? 'Bản ghi đã hoàn tất' : turn ? `Gợi ý ${turn.action === 'ban' ? 'cấm' : 'chọn'}` : 'Sẵn sàng cho ván tiếp theo'}</h2></div></div>
          {!archive && turn && <>
            <div className="recommend-meta"><span>Top {view?.recommendations.length || 0} · {view?.configuration.lane_review_policy ? 'Xét giữ cặp / kèo đủ mẫu, rồi điểm gốc' : 'Điểm ưu tiên, không phải % thắng'}</span>{turn.action === 'pick' && <select aria-label="Lọc vị trí gợi ý" value={onlyRole || ''} disabled={busy} onChange={e => void submit('/draft/view', session, {}, (e.target.value || null) as Role | null)}><option value="">Mọi vị trí trống</option>{ROLES.filter(r => !game?.picks[turn.side][r]).map(r => <option key={r} value={r}>{ROLE[r]}</option>)}</select>}</div>
              <div className="candidate-list">{view?.recommendations.map((row, index) => <button key={`${row.champion}:${row.role}`} data-testid={`candidate-${index}`} className={`candidate ${!manual && selected?.champion === row.champion && selected.role === row.role ? 'selected' : ''}`} disabled={busy} onClick={() => { const deselect = !manual && selected?.champion === row.champion && selected.role === row.role; setManual(false); setSelected(deselect ? null : row); setInspection(null); setInspectorOpen(!deselect) }}><span className="rank">{String(index + 1).padStart(2, '0')}</span><Portrait name={row.champion} lookup={lookup} small /><div className="candidate-copy"><strong>{label(row.champion)}</strong><small>{row.role ? `${ROLE[row.role]} · ${row.games ?? 0} trận` : 'Pool ban theo lịch sử'}</small>{laneSummary(row) && <small className="lane-summary">{laneSummary(row)}</small>}</div>{row.pair_reservation?.status === 'secure_now' ? <span className="badge">Giữ cặp trước ban</span> : row.lane_review?.status === 'observed_lane' ? <span className="badge">Kèo đủ mẫu</span> : row.evidence_status === 'sparse_candidate' ? <span className="badge warning-text">Ít mẫu</span> : row.review_required ? <span className="badge warning-text">Thiếu đối đầu</span> : null}<b className="candidate-score">{points(row)}<small>điểm gốc</small></b></button>)}</div>
              {!view?.recommendations.length && <p className="empty-copy">Không có gợi ý đủ điều kiện trong pool này. Bạn có thể chọn tay.</p>}
            <div className="action-row"><button className={`primary ${turn.side}`} disabled={busy || !selected} onClick={() => void submit('/draft/action', session, { champion: selected?.champion, role: turn.action === 'pick' ? selected?.role : null })}>{busy && !automating ? 'Đang tính…' : `${turn.action === 'ban' ? 'Cấm' : 'Chọn'} ${selected ? label(selected.champion) : 'tướng'}${selected?.role ? ` · ${ROLE[selected.role]}` : ''}`}</button>{automating ? <button className="outline" onClick={() => { autoRef.current = false }}>Dừng sau lượt này</button> : <button className="outline" disabled={busy || !view?.recommendations.length} onClick={() => void autoGame()}>Tự draft ván</button>}</div>
          </>}
          {archive && <p className="empty-copy">Ván này chỉ để xem lại. Chọn ván {activeIndex + 1} để tiếp tục thao tác.</p>}
          {!archive && !turn && view && <div className="complete-state"><span className="complete-mark">✓</span><div><strong>{view.series_complete ? 'Đủ 5 ván draft Fearless' : 'Đội hình đã đủ 5 vị trí'}</strong><p>Chọn đội đi trước và sang ván tại phần thiết lập trên đầu trang.</p></div></div>}
        </section>

        {!archive && turn && <section className="panel manual-choice" aria-label="Chọn tướng thủ công"><span className="eyebrow">LỰA CHỌN CỦA BẠN</span><h2>Chọn tay</h2><p className="micro">Tìm và xác nhận tướng riêng, đồng thời đối chiếu với danh sách gợi ý ở trên.</p>
          <div className="manual-controls"><label>Tìm tướng<input aria-label="Tìm tướng" value={search} onChange={e => setSearch(e.target.value)} placeholder="Tên tướng…" /></label></div>
          {turn.action === 'pick' && <p className="placement-note" data-testid="manual-placement">{manualName ? manualPlacement ? `Tự xếp ${ROLE[manualPlacement.role]} · ${manualPlacement.games} lần quan sát. Bỏ qua các vị trí đã có tướng; có thể kéo đổi sau khi chọn.` : 'Không có vị trí đã quan sát còn trống. Kéo đổi đội hình để tạo chỗ hoặc chọn tướng khác.' : 'Tự xếp vào vị trí phổ biến nhất còn trống theo dữ liệu Pro của phiên.'}</p>}
          <div className="champion-grid">{catalog?.champions.filter(c => `${c.label} ${c.name}`.toLocaleLowerCase().includes(search.toLocaleLowerCase())).map(c => <button key={c.name} title={unavailable.has(c.name) ? 'Đã cấm, chọn hoặc khóa Fearless' : c.label} className={manualName === c.name ? 'selected' : ''} disabled={busy || unavailable.has(c.name)} onClick={() => { const deselect = manual && manualName === c.name; setManual(true); setManualName(deselect ? '' : c.name); setSelected(null); setInspection(null); setInspectorOpen(!deselect) }}><Portrait name={c.name} lookup={lookup} small /><span>{c.label}</span></button>)}</div>
          <div className="action-row"><button className={`primary ${turn.side}`} disabled={busy || !manualName || (turn.action === 'pick' && !manualRole)} onClick={() => void submit('/draft/action', session, { champion: manualName, role: null })}>{turn.action === 'ban' ? 'Xác nhận cấm' : 'Xác nhận chọn'} {manualName ? label(manualName) : 'tướng'}{turn.action === 'pick' && manualRole ? ` · ${ROLE[manualRole]}` : ''}</button></div>
        </section>}

        <section className="panel timeline"><div className="section-line"><h2>Diễn biến ván {displayIndex + 1}</h2><button className="quiet" disabled={busy || archive || !session.current.history.length} onClick={undo}>← Hoàn tác ban/pick</button></div><p className="micro">Bấm vào một lượt để tính lại bằng chứng từ trạng thái trước lượt đó.</p><div className="timeline-grid">{view?.schedule.map(step => { const move = game?.history[step.turn - 1]; return <button key={step.turn} className={`timeline-step ${step.side} ${move ? 'done' : ''} ${turn?.turn === step.turn ? 'now' : ''}`} disabled={busy || !move} onClick={() => void inspectTurn(step.turn)} title={move ? `${names[step.side]} ${step.action} ${step.number}: ${label(move.champion)}` : `Lượt ${step.turn}`}><span>{step.turn.toString().padStart(2, '0')} · {step.action === 'ban' ? 'B' : 'P'}{step.number}</span>{move ? <Portrait name={move.champion} lookup={lookup} small /> : <i>—</i>}</button> })}</div></section>
      </main>

      {!inspectorOpen && (selected || manualName || inspection) && <button className="outline inspector-reopen" onClick={() => setInspectorOpen(true)}>Mở hiểu lựa chọn</button>}
      {inspectorOpen && <Inspector onClose={() => setInspectorOpen(false)} advice={inspection ? inspection.advice : archive || manual && manualName ? null : selected} title={inspection ? `${label(inspection.move.champion)} · lượt ${inspection.move.turn}` : archive ? `Lịch sử ván ${displayIndex + 1}` : manual && manualName ? label(manualName) : selected ? label(selected.champion) : 'Vì sao chọn tướng này?'} notice={inspection?.notice || (archive ? 'Bấm một lượt ban/pick trong lịch sử để xem căn cứ tại thời điểm đó.' : manual && manualName ? 'Đây là lựa chọn tay. Sau khi chọn, bấm vào lượt trong lịch sử để xem bằng chứng nếu có.' : undefined)} />}
    </div>
    <footer className="page-footer"><span>DRAFTLAB <b>·</b> Minh họa ứng dụng khoa học dữ liệu</span><span>Công thức hiện hành · Rank chỉ là bằng chứng bổ sung · Không tối ưu toàn BO5</span></footer>
  </div>
}
