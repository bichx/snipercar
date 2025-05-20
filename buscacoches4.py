import asyncio
from playwright.async_api import async_playwright
import json

async def obtener_marcas():
    print("🚀 Iniciando navegador y escuchando tráfico XHR...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="es-ES",
            java_script_enabled=True
        )
        page = await context.new_page()

        marcas_capturadas = []

        async def interceptar(response):
            url = response.url
            if "/vo/api/makes" in url:
                try:
                    print(f"📡 Interceptado: {url}")
                    json_data = await response.json()
                    for marca in json_data:
                        marcas_capturadas.append({"id": marca.get("id"), "marca": marca.get("name")})
                except Exception as e:
                    print(f"❌ Error procesando JSON de marcas: {e}")

        page.on("response", interceptar)

        await page.goto("https://www.coches.net/segunda-mano/", timeout=60000)
        await page.wait_for_timeout(4000)

        try:
            await page.click("button[data-testid='search-form__make-button']")
            await page.wait_for_timeout(5000)
        except Exception as e:
            print(f"⚠️ Error interactuando con la página: {e}")

        await page.wait_for_timeout(5000)
        await browser.close()

        return marcas_capturadas

async def main():
    marcas = await obtener_marcas()
    if not marcas:
        print("❌ No se capturó ninguna marca.")
    else:
        print(json.dumps(marcas, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
