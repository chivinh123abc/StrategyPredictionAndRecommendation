import { test, expect } from '@playwright/test'
import { mkdir } from 'node:fs/promises'

test('real draft: ban/pick, evidence, flex, undo, next game, export and restore', async ({ page }) => {
  const browserErrors: string[] = []
  page.on('pageerror', error => browserErrors.push(error.message))
  await page.goto('/')
  await expect(page.getByTestId('candidate-0')).toBeVisible()
  await expect(page.getByText('Mỗi lượt chọn, một căn cứ.')).toBeVisible()
  await expect(page.getByTestId('current-turn')).toContainText('cấm 1')
  await expect(page.getByRole('region', { name: 'Chọn tướng thủ công' })).toBeVisible()
  await expect(page.getByRole('region', { name: 'Gợi ý từ hệ thống' })).toBeVisible()
  await expect(page.getByTestId('configuration')).toContainText('current')
  const setupBox = await page.locator('.setup').boundingBox()
  const recommendationBox = await page.locator('.recommendations').boundingBox()
  const manualBox = await page.locator('.manual-choice').boundingBox()
  await expect(page.locator('.inspector')).toHaveCount(0)
  expect(setupBox!.y + setupBox!.height).toBeLessThan(recommendationBox!.y)
  expect(Math.abs(recommendationBox!.y - manualBox!.y)).toBeLessThan(2)
  expect(recommendationBox!.x).toBeLessThan(manualBox!.x)
  const boardsBox = await page.locator('.teams-grid').boundingBox()
  expect(recommendationBox!.x + recommendationBox!.width).toBeLessThan(boardsBox!.x)
  expect(boardsBox!.x + boardsBox!.width).toBeLessThan(manualBox!.x)

  const identity = await page.getByTestId('configuration').locator('code').textContent()

  async function commitSelection() {
    await page.getByTestId('candidate-0').click()
    const response = page.waitForResponse(r => r.url().endsWith('/api/draft/action'))
    await page.locator('.recommendations .action-row .primary').click()
    expect((await response).status()).toBe(200)
    await expect(page.getByTestId('candidate-0')).toBeEnabled()
  }

  const manual = page.getByRole('region', { name: 'Chọn tướng thủ công' })
  const firstBan = (await page.getByTestId('candidate-0').locator('.candidate-copy strong').textContent())!
  await manual.getByLabel('Tìm tướng').fill(firstBan)
  await manual.getByRole('button', { name: firstBan, exact: true }).click()
  const manualResponse = page.waitForResponse(r => r.url().endsWith('/api/draft/action'))
  await manual.getByRole('button', { name: `Xác nhận cấm ${firstBan}` }).click()
  expect((await manualResponse).status()).toBe(200)
  await expect(page.getByTestId('candidate-0')).toBeEnabled()
  for (let index = 0; index < 5; index++) await commitSelection()
  await expect(page.getByTestId('current-turn')).toContainText('chọn 1')
  const filtered = page.waitForResponse(r => r.url().endsWith('/api/draft/view'))
  await page.getByLabel('Lọc vị trí gợi ý').selectOption('mid')
  expect((await filtered).status()).toBe(200)
  await expect(page.getByTestId('candidate-0')).toBeEnabled()
  await commitSelection()
  await page.getByTestId('candidate-0').click()
  await expect(page.getByTestId('source-comparison').first()).toBeVisible()
  await expect(page.locator('.source-table').first()).toContainText('Pro')
  await expect(page.locator('.source-table').first()).toContainText('Rank')

  const blue = page.getByRole('region', { name: 'Bảng đội xanh' })
  const name = (await blue.locator('.role-slot.filled .slot-copy strong').textContent())!
  const swapped = page.waitForResponse(r => r.url().endsWith('/api/draft/swap'))
  await page.getByTestId('slot-blue-mid').dragTo(page.getByTestId('slot-blue-top'))
  expect((await swapped).status()).toBe(200)
  await expect(blue.locator('.role-slot').first()).toContainText(name)
  await expect(page.getByTestId('candidate-0')).toBeEnabled()

  const undone = page.waitForResponse(r => r.url().endsWith('/api/draft/view'))
  await page.getByRole('button', { name: /Hoàn tác ban\/pick/ }).click()
  expect((await undone).status()).toBe(200)
  await expect(blue.locator('.role-slot.filled')).toHaveCount(0)
  await commitSelection()
  await mkdir('../reports/ui_lane_revision', { recursive: true })
  await page.screenshot({ path: '../reports/ui_inspector_toggle/desktop.png', fullPage: true })

  const allowed = page.waitForResponse(r => r.url().endsWith('/api/draft/view'))
  await page.getByRole('checkbox', { name: /Cho phép chọn thiếu bằng chứng/ }).check()
  expect((await allowed).status()).toBe(200)
  await expect(page.getByRole('button', { name: 'Tự draft ván' })).toBeEnabled()
  await page.getByRole('button', { name: 'Tự draft ván' }).click()
  await expect(page.getByRole('button', { name: /Sang ván 2/ })).toBeVisible({ timeout: 120_000 })
  await expect(page.locator('.role-slot.filled')).toHaveCount(10)

  await expect(page.getByRole('button', { name: /Sang ván 2/ })).toBeDisabled()
  await page.getByLabel('Đội chọn trước ván tiếp theo').selectOption('blue')
  await page.getByRole('button', { name: /Sang ván 2/ }).click()
  await expect(page.getByTestId('current-turn')).toContainText('VÁN 2 / 5')
  await expect(page.getByTestId('current-turn')).toContainText('T1')
  await expect(page.locator('.setup .muted')).toContainText('10 tướng bị khóa')
  await page.getByLabel('Các ván draft').getByRole('button').nth(0).click()
  await expect(page.getByRole('complementary', { name: 'Bằng chứng gợi ý' })).toHaveCount(0)
  await page.getByLabel('Các ván draft').getByRole('button').nth(1).click()
  const downloaded = page.waitForEvent('download')
  await page.getByRole('button', { name: /Xuất JSON/ }).click()
  const exported = await downloaded
  expect(exported.suggestedFilename()).toBe('draft-lab-bo5.json')
  await exported.saveAs('../reports/ui_inspector_toggle/export.json')
  await page.reload()
  await expect(page.getByTestId('candidate-0')).toBeVisible()
  await expect(page.getByTestId('current-turn')).toContainText('VÁN 2 / 5')
  await page.setViewportSize({ width: 390, height: 844 })
  await page.screenshot({ path: '../reports/ui_inspector_toggle/mobile.png', fullPage: true })
  await expect(page.getByTestId('configuration').locator('code')).toHaveText(identity!)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
  expect(browserErrors).toEqual([])
})

test('changed snapshot preserves input export and can start a fresh session', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByTestId('candidate-0')).toBeVisible()
  await page.evaluate(() => {
    const saved = JSON.parse(localStorage.getItem('draft-lab-session-v1')!)
    saved.session.snapshot_id = '0'.repeat(64)
    localStorage.setItem('draft-lab-session-v1', JSON.stringify(saved))
  })
  await page.reload()
  await expect(page.getByRole('alert')).toContainText('Dữ liệu hoặc cấu hình phiên đã thay đổi')
  await expect(page.getByRole('button', { name: /Xuất JSON/ })).toBeEnabled()
  await page.getByRole('button', { name: /Phiên mới/ }).click()
  await expect(page.getByTestId('candidate-0')).toBeVisible()
  await expect(page.getByLabel('Tìm tướng')).toBeVisible()
})

test('Red may select first; exposed bot lane displays partner reservation', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByTestId('candidate-0')).toBeVisible()
  await page.getByLabel('Đội chọn trước', {exact: true}).selectOption('red')
  await expect(page.getByTestId('current-turn')).toContainText('Gen.G')
  const history = [
    ['blue','ban','Qiyana',null],['red','ban','Nocturne',null],
    ['blue','ban','Olaf',null],['red','ban','Vi',null],
    ['blue','ban','Ezreal',null],['red','ban','Lee Sin',null],
    ['blue','pick','Cassiopeia','mid'],['red','pick','Renata Glasc','sup'],
    ['red','pick','Kalista','bot'],['blue','pick','Nautilus','sup'],
  ].map(([side,action,champion,role]) => ({side,action,champion,role}))
  const session = {settings:{region:'WLDS',blue_team:'T1',red_team:'Gen.G',ban_strategy:'contextual',as_of:'2026-11-24',allow_statistical_auto:false},completed:[],current:{first_side:'blue',history,swaps:[]}}
  const response = await page.request.post('/api/draft/view', {data:{session}})
  expect(response.status()).toBe(200)
  const validated = (await response.json()).session
  await page.evaluate(value => localStorage.setItem('draft-lab-session-v1',JSON.stringify({version:1,session:value})),validated)
  await page.reload()
  await expect(page.getByTestId('candidate-0')).toContainText('Xạ thủ')
  await page.getByTestId('candidate-0').click()
  await expect(page.getByRole('complementary', {name:'Bằng chứng gợi ý'})).toContainText('Ưu tiên giữ cặp bot')
  await page.screenshot({path:'../reports/ui_inspector_toggle/pair-window.png',fullPage:true})
  await page.getByLabel('Lọc vị trí gợi ý').selectOption('top')
  await expect(page.getByTestId('candidate-0')).toBeEnabled()
  await page.getByTestId('candidate-0').click()
  await expect(page.getByRole('complementary', {name:'Bằng chứng gợi ý'})).toContainText('Có thể mất toàn bộ nhóm này')
})

test('manual placement skips occupied popular role and drag swaps occupied slots', async ({ page }) => {
  const history = [
    ['blue','ban','Qiyana',null],['red','ban','Nocturne',null],['blue','ban','Olaf',null],
    ['red','ban','Vi',null],['blue','ban','Ezreal',null],['red','ban','Lee Sin',null],
    ['blue','pick','Cassiopeia','mid'],['red','pick','Renata Glasc','sup'],['red','pick','Kalista','bot'],
  ].map(([side,action,champion,role]) => ({side,action,champion,role}))
  await page.goto('/')
  const response = await page.request.post('/api/draft/view',{data:{session:{settings:{as_of:'2026-11-24'},current:{first_side:'blue',history,swaps:[]},completed:[]}}})
  expect(response.status()).toBe(200)
  await page.evaluate(session => localStorage.setItem('draft-lab-session-v1',JSON.stringify({version:1,session})),(await response.json()).session)
  await page.reload()
  await expect(page.getByLabel('Vị trí chọn tay')).toHaveCount(0)
  const manual = page.getByRole('region',{name:'Chọn tướng thủ công'})
  await manual.getByLabel('Tìm tướng').fill('Galio')
  await manual.getByRole('button',{name:'Galio',exact:true}).click()
  await expect(page.getByTestId('manual-placement')).toContainText('Tự xếp Top')
  const picked = page.waitForResponse(r => r.url().endsWith('/api/draft/action'))
  await manual.getByRole('button',{name:'Xác nhận chọn Galio · Top',exact:true}).click()
  expect((await picked).status()).toBe(200)
  await expect(page.getByTestId('slot-blue-top')).toContainText('Galio')
  await expect(page.getByTestId('slot-blue-mid')).toContainText('Cassiopeia')
  const swapped = page.waitForResponse(r => r.url().endsWith('/api/draft/swap'))
  await page.getByTestId('slot-blue-top').dragTo(page.getByTestId('slot-blue-mid'))
  expect((await swapped).status()).toBe(200)
  await expect(page.getByTestId('slot-blue-top')).toContainText('Cassiopeia')
  await expect(page.getByTestId('slot-blue-mid')).toContainText('Galio')
  await page.getByTestId('slot-blue-mid').dragTo(page.getByTestId('slot-red-top'))
  await expect(page.getByRole('alert')).toContainText('Chỉ đổi vị trí tướng trong cùng một đội')
  await expect(page.getByTestId('slot-blue-mid')).toContainText('Galio')
  await page.screenshot({path:'../reports/ui_inspector_toggle/drag-and-auto-role.png',fullPage:true})
})

test('late top suggestion exposes Galio zero samples and Renekton two-game winrate', async ({ page }) => {
  const first = [
    ['blue','ban','Qiyana',null],['red','ban','Nocturne',null],['blue','ban','Olaf',null],
    ['red','ban','Vi',null],['blue','ban','Ezreal',null],['red','ban','Lee Sin',null],
    ['blue','pick','Cassiopeia','mid'],['red','pick','Renata Glasc','sup'],['red','pick','Kalista','bot'],
    ['blue','pick','Nautilus','sup'],['blue','pick','Jhin','bot'],['red','pick','Orianna','mid'],
    ['red','ban','Jayce',null],['blue','ban','Jarvan IV',null],['red','ban','Rumble',null],
    ['blue','ban','Pantheon',null],['red','pick','Ambessa','top'],['blue','pick','Wukong','jng'],
  ].map(([side,action,champion,role]) => ({side,action,champion,role}))
  await page.goto('/')
  const response=await page.request.post('/api/draft/view',{data:{session:{settings:{as_of:'2026-11-24'},current:{history:first,swaps:[],first_side:'blue'},completed:[]}}})
  expect(response.status()).toBe(200)
  await page.evaluate(session => localStorage.setItem('draft-lab-session-v1',JSON.stringify({version:1,session})),(await response.json()).session)
  await page.reload()
  await expect(page.getByTestId('candidate-0')).toContainText('Gnar')
  await page.locator('.candidate').filter({hasText:'Galio'}).click()
  await expect(page.getByTestId('lane-review')).toContainText('0 mẫu Pro')
  await page.locator('.candidate').filter({hasText:'Renekton'}).click()
  await expect(page.getByTestId('lane-review')).toContainText('2 mẫu Pro')
  await expect(page.locator('.candidate').filter({hasText:'Renekton'})).toContainText('WR trận 100.0%')
  await expect(page.locator('.candidate').filter({hasText:'Renekton'})).toContainText('GD15 +787')
  await page.screenshot({path:'../reports/ui_inspector_toggle/lane-audit.png',fullPage:true})
})
