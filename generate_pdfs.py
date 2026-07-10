import os
import urllib.request
from playwright.sync_api import sync_playwright

# 1. 크롤링할 제주 드림타워 URL 목록 (총 15개)
MENU_CONFIGS = [
    # 델리 (Deli) 5개 언어
    {"name": "Deli_KOR", "url": "https://www.jejudreamtower.com/kor/dine/Deli.jdt"},
    {"name": "Deli_ENG", "url": "https://www.jejudreamtower.com/eng/dine/Deli.jdt"},
    {"name": "Deli_CHI", "url": "https://www.jejudreamtower.com/chi/dine/Deli.jdt"},
    {"name": "Deli_ZHO", "url": "https://www.jejudreamtower.com/zho/dine/Deli.jdt"},
    {"name": "Deli_JPN", "url": "https://www.jejudreamtower.com/jpn/dine/Deli.jdt"},
    
    # 그랜드 키친 (Grand Kitchen) 5개 언어
    {"name": "GrandKitchen_KOR", "url": "https://www.jejudreamtower.com/kor/dine/GrandKitchen.jdt"},
    {"name": "GrandKitchen_ENG", "url": "https://www.jejudreamtower.com/eng/dine/GrandKitchen.jdt"},
    {"name": "GrandKitchen_CHI", "url": "https://www.jejudreamtower.com/chi/dine/GrandKitchen.jdt"},
    {"name": "GrandKitchen_ZHO", "url": "https://www.jejudreamtower.com/zho/dine/GrandKitchen.jdt"},
    {"name": "GrandKitchen_JPN", "url": "https://www.jejudreamtower.com/jpn/dine/GrandKitchen.jdt"},
    
    # 드림푸드코트 (PopUpPlaza) 5개 언어
    {"name": "PopUpPlaza_KOR", "url": "https://www.jejudreamtower.com/kor/dine/PopUpPlaza.jdt"},
    {"name": "PopUpPlaza_ENG", "url": "https://www.jejudreamtower.com/eng/dine/PopUpPlaza.jdt"},
    {"name": "PopUpPlaza_CHI", "url": "https://www.jejudreamtower.com/chi/dine/PopUpPlaza.jdt"},
    {"name": "PopUpPlaza_ZHO", "url": "https://www.jejudreamtower.com/zho/dine/PopUpPlaza.jdt"},
    {"name": "PopUpPlaza_JPN", "url": "https://www.jejudreamtower.com/jpn/dine/PopUpPlaza.jdt"}
]

# 2. PDF가 저장될 전용 폴더 생성
OUTPUT_DIR = "pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_pdfs():
    with sync_playwright() as p:
        # 가상의 크롬 브라우저 실행 (화면을 띄우지 않고 백그라운드에서 실행)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🚀 제주 드림타워 원본 PDF 크롤링 봇 작동 시작!\n" + "="*50)

        for config in MENU_CONFIGS:
            file_name = f"{config['name']}.pdf"
            file_path = os.path.join(OUTPUT_DIR, file_name)
            target_url = config['url']

            print(f"▶ 타겟 접속 중: {config['name']} ...")

            try:
                # 1. 제주 드림타워 웹페이지 접속
                # 네트워크 통신이 안정될 때까지 기다립니다.
                page.goto(target_url, wait_until="networkidle")

                # 2. PDF 링크 찾기 (핵심 변경점 ⭐)
                # 외국어 페이지에서는 '메뉴 다운로드'라는 글씨가 다를 수 있으므로, 
                # 글씨에 상관없이 링크 주소가 '.pdf'로 끝나는 요소를 무조건 찾도록 변경했습니다.
                pdf_element = page.locator("a[href$='.pdf']")
                
                # 버튼이 화면에 여러 개일 수 있으니 첫 번째 버튼의 속성(href)을 가져옵니다.
                pdf_url = pdf_element.first.get_attribute("href")

                if pdf_url:
                    print(f"   -> 원본 주소 발견: {pdf_url.split('/')[-1]} (숫자 무시하고 무조건 최신본)")
                    print(f"   -> 파일 다운로드 진행 중...")
                    
                    # 3. 발견한 진짜 PDF 주소로 직접 접속하여 파일을 내 컴퓨터/서버로 저장!
                    urllib.request.urlretrieve(pdf_url, file_path)
                    print(f"   ✅ 완료: {file_name} 저장 성공!\n")
                else:
                    print(f"   ❌ 실패: '메뉴 다운로드' 버튼을 찾을 수 없습니다.\n")

            except Exception as e:
                print(f"   ❌ 에러 발생: 작업 중 통신 오류 - {e}\n")

        print("="*50 + "\n🎉 모든 메뉴판 크롤링 및 다운로드가 완료되었습니다!")
        browser.close()

if __name__ == "__main__":
    generate_pdfs()
