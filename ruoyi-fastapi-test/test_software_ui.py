import pytest
from playwright.async_api import async_playwright

from common.config import Config


def _is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    import socket

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


@pytest.mark.asyncio
async def test_admin_software_menu_and_list_render() -> None:
    """
    管理端：验证「软件管理」一级菜单可见，且「软件列表」能渲染出种子数据（如 Python）
    """
    if not _is_port_open("127.0.0.1", 80):
        pytest.skip("admin frontend is not running on http://localhost:80")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Login
        await page.goto(Config.frontend_url + "/login")
        await page.wait_for_selector('input[placeholder="账号"]')
        await page.fill('input[placeholder="账号"]', "admin")
        await page.fill('input[placeholder="密码"]', "admin123")
        # The login button text may contain a space (e.g. "登 录"), so prefer type selector
        try:
            await page.click('button[type="submit"]', timeout=5000)
        except Exception:
            await page.click("button")

        await page.wait_for_url("**/index**", timeout=15000)

        # Sidebar -> 软件管理 -> 软件列表
        await page.wait_for_selector("text=软件管理", timeout=15000)
        await page.click("text=软件管理")
        await page.click("text=软件列表")

        # Search for a seeded item to make the test stable across pagination
        await page.wait_for_selector('input[placeholder="请输入软件名称"]', timeout=15000)
        await page.fill('input[placeholder="请输入软件名称"]', "Python")
        await page.click('button:has-text("搜索")')

        await page.wait_for_selector("text=Python", timeout=15000)

        await browser.close()


@pytest.mark.asyncio
async def test_portal_h5_software_list_and_detail_render() -> None:
    """
    用户端 H5：验证软件库列表页与详情页渲染（依赖 `pnpm dev:h5` 已启动）
    """
    if not _is_port_open("127.0.0.1", 9090):
        pytest.skip("H5 server is not running on http://localhost:9090 (run `pnpm dev:h5`)")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Uni-app H5 default route uses hash router
        await page.goto("http://localhost:9090/#/pages/software/index")
        await page.wait_for_load_state("networkidle")

        await page.wait_for_selector("text=软件库", timeout=15000)

        # Search keyword to make it stable
        await page.fill('input[type="search"]', "Python")
        await page.click('text="搜索"')
        await page.wait_for_selector("text=Python", timeout=15000)

        # Click entry -> detail page
        await page.click("text=Python")
        await page.wait_for_url("**/pages/software/detail**", timeout=15000)
        await page.wait_for_selector('text=多平台下载', timeout=15000)

        await browser.close()
