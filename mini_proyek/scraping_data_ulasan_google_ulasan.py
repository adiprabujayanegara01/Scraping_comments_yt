"""
Google Maps Review Scraper - ENHANCED VERSION
Optimized untuk scraping 7000+ ulasan

Install dependencies:
pip install selenium webdriver-manager pandas openpyxl
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
from datetime import datetime

class GoogleMapsReviewScraper:
    def __init__(self, headless=False):
        """Inisialisasi Chrome driver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--lang=id')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--disable-features=VizDisplayCompositor')
        
        if headless:
            options.add_argument('--headless')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
    
    def find_scrollable_element(self):
        """Cari elemen yang bisa di-scroll dengan berbagai cara"""
        print("🔍 Mencari scrollable element...")
        
        # Method 1: Cari berdasarkan class yang umum untuk panel ulasan
        possible_selectors = [
            "//div[contains(@class, 'm6QErb') and contains(@class, 'DxyBCb')]",
            "//div[@role='main']//div[contains(@style, 'overflow')]",
            "//div[contains(@class, 'DxyBCb')]",
            "//div[@class='m6QErb DxyBCb kA9KIf dS8AEf ']",
        ]
        
        for selector in possible_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for elem in elements:
                    scroll_height = self.driver.execute_script(
                        "return arguments[0].scrollHeight;", elem
                    )
                    client_height = self.driver.execute_script(
                        "return arguments[0].clientHeight;", elem
                    )
                    
                    if scroll_height > client_height and client_height > 0:
                        print(f"✅ Ditemukan scrollable element dengan selector: {selector}")
                        print(f"   ScrollHeight: {scroll_height}, ClientHeight: {client_height}")
                        return elem
            except Exception as e:
                continue
        
        # Method 2: Cari semua div dengan overflow-y
        print("🔍 Mencoba method 2: mencari div dengan overflow...")
        try:
            all_divs = self.driver.find_elements(By.TAG_NAME, "div")
            for div in all_divs:
                try:
                    overflow_y = div.value_of_css_property("overflow-y")
                    if overflow_y in ["auto", "scroll"]:
                        scroll_height = self.driver.execute_script(
                            "return arguments[0].scrollHeight;", div
                        )
                        client_height = self.driver.execute_script(
                            "return arguments[0].clientHeight;", div
                        )
                        
                        if scroll_height > client_height and client_height > 300:
                            print(f"✅ Ditemukan dengan overflow property")
                            print(f"   ScrollHeight: {scroll_height}, ClientHeight: {client_height}")
                            return div
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Method 2 gagal: {e}")
        
        print("❌ Tidak dapat menemukan scrollable element!")
        return None
    
    def scroll_reviews_panel(self, max_scrolls=3000, target_reviews=7000):
        """
        Scroll panel ulasan sampai mencapai target atau tidak ada lagi ulasan baru
        ENHANCED: Untuk 7000+ ulasan
        """
        print(f"\n{'='*60}")
        print("🔄 MEMULAI PROSES SCROLL ENHANCED")
        print(f"   Target ulasan: {target_reviews}")
        print(f"   Max scrolls: {max_scrolls}")
        print(f"{'='*60}\n")
        
        try:
            time.sleep(3)
            
            scrollable = self.find_scrollable_element()
            
            if not scrollable:
                print("❌ Tidak dapat menemukan scrollable element, mencoba scroll window...")
                scrollable = self.driver.find_element(By.TAG_NAME, "body")
            
            last_height = 0
            scroll_count = 0
            no_change_count = 0
            total_reviews_before = 0
            consecutive_same = 0
            last_check_time = time.time()
            
            # Statistik untuk monitoring
            scroll_stats = {
                'last_100_scrolls': [],
                'avg_new_reviews_per_scroll': 0
            }
            
            while scroll_count < max_scrolls:
                # Hitung jumlah ulasan sebelum scroll
                try:
                    current_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf'))
                except:
                    current_reviews = 0
                
                # Cek apakah sudah mencapai target
                if current_reviews >= target_reviews:
                    print(f"\n🎯 TARGET TERCAPAI! {current_reviews} ulasan (target: {target_reviews})")
                    break
                
                # Scroll ke bawah dengan variasi kecepatan
                scroll_amount = self.driver.execute_script(
                    'return arguments[0].scrollHeight',
                    scrollable
                )
                
                # Scroll bertahap untuk memastikan loading
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight',
                    scrollable
                )
                
                scroll_count += 1
                
                # Progress indicator lebih detail
                if scroll_count % 10 == 0 or current_reviews != total_reviews_before:
                    elapsed = time.time() - last_check_time
                    rate = (current_reviews - total_reviews_before) / elapsed if elapsed > 0 else 0
                    print(f"📜 Scroll #{scroll_count}/{max_scrolls} | Ulasan: {current_reviews}/{target_reviews} | Rate: {rate:.1f}/s")
                    last_check_time = time.time()
                
                # Tunggu loading dengan waktu dinamis
                # Lebih lama jika banyak ulasan untuk loading
                if current_reviews > 3000:
                    time.sleep(2.0)
                elif current_reviews > 1000:
                    time.sleep(1.5)
                else:
                    time.sleep(1.2)
                
                # Cek tinggi baru
                new_height = self.driver.execute_script(
                    'return arguments[0].scrollHeight',
                    scrollable
                )
                
                # Hitung ulasan setelah scroll
                try:
                    reviews_after = len(self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf'))
                except:
                    reviews_after = 0
                
                # Update statistik
                new_reviews = reviews_after - total_reviews_before
                scroll_stats['last_100_scrolls'].append(new_reviews)
                if len(scroll_stats['last_100_scrolls']) > 100:
                    scroll_stats['last_100_scrolls'].pop(0)
                
                # Cek apakah ada perubahan
                if new_height == last_height and reviews_after == total_reviews_before:
                    no_change_count += 1
                    consecutive_same += 1
                    print(f"⏸️  Tidak ada perubahan ({no_change_count}/100) - Ulasan: {reviews_after}")
                    
                    # Strategi recovery jika stuck - lebih agresif
                    if consecutive_same >= 5:
                        print("   🔄 Strategi recovery #1: Scroll mundur...")
                        # Scroll ke atas sedikit lalu ke bawah lagi
                        self.driver.execute_script(
                            'arguments[0].scrollTop = arguments[0].scrollTop - 1000',
                            scrollable
                        )
                        time.sleep(1.5)
                        self.driver.execute_script(
                            'arguments[0].scrollTop = arguments[0].scrollHeight',
                            scrollable
                        )
                        time.sleep(2.5)
                        consecutive_same = 0
                    
                    # Recovery tambahan untuk kasus stuck parah
                    if no_change_count == 25:
                        print("   🔄 Strategi recovery #2: Multiple rapid scrolls...")
                        for i in range(10):
                            self.driver.execute_script(
                                'arguments[0].scrollTop = arguments[0].scrollHeight',
                                scrollable
                            )
                            time.sleep(0.5)
                        time.sleep(3)
                    
                    if no_change_count == 50:
                        print("   🔄 Strategi recovery #3: Deep scroll dengan pause...")
                        # Scroll ke tengah
                        self.driver.execute_script(
                            'arguments[0].scrollTop = arguments[0].scrollHeight / 2',
                            scrollable
                        )
                        time.sleep(2)
                        # Scroll ke bawah lagi
                        for i in range(15):
                            self.driver.execute_script(
                                'arguments[0].scrollTop = arguments[0].scrollHeight',
                                scrollable
                            )
                            time.sleep(1)
                    
                    if no_change_count == 75:
                        print("   🔄 Strategi recovery #4: Extreme measures...")
                        # Refresh scrollable element
                        scrollable = self.find_scrollable_element()
                        time.sleep(2)
                        # Aggressive scrolling
                        for i in range(20):
                            self.driver.execute_script(
                                'arguments[0].scrollTop = arguments[0].scrollHeight',
                                scrollable
                            )
                            time.sleep(0.8)
                    
                    # Hanya stop jika benar-benar tidak ada perubahan dalam waktu SANGAT lama
                    if no_change_count >= 100:  # Sangat toleran: 100x cek
                        print(f"\n✅ SCROLL SELESAI (Tidak ada ulasan baru setelah 100x cek)")
                        print(f"   Total scroll: {scroll_count}")
                        print(f"   Total ulasan yang dimuat: {reviews_after}")
                        
                        # Verifikasi akhir dengan scroll ekstra super agresif
                        print("   🔍 Verifikasi akhir ULTIMATE dengan scroll ekstra...")
                        for round in range(3):
                            print(f"      Round {round+1}/3...")
                            for _ in range(10):
                                self.driver.execute_script(
                                    'arguments[0].scrollTop = arguments[0].scrollHeight',
                                    scrollable
                                )
                                time.sleep(1.5)
                            time.sleep(3)
                        
                        final_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf'))
                        if final_count > reviews_after:
                            print(f"   ⚠️ Ditemukan {final_count - reviews_after} ulasan tambahan! Melanjutkan...")
                            no_change_count = 0
                            continue
                        else:
                            print(f"   ✅ Verifikasi selesai. Total final: {final_count}")
                            break
                else:
                    if reviews_after > total_reviews_before:
                        new_count = reviews_after - total_reviews_before
                        percentage = (reviews_after / target_reviews) * 100
                        print(f"   ✅ +{new_count} ulasan baru! Total: {reviews_after} ({percentage:.1f}% dari target)")
                    no_change_count = 0
                    consecutive_same = 0
                    last_height = new_height
                    total_reviews_before = reviews_after
                
                # Scroll ekstra agresif jika mendekati stuck
                if no_change_count >= 15 and no_change_count < 100:
                    if no_change_count % 10 == 0:  # Setiap 10x no change
                        print(f"   🔄 Auto recovery: Multiple aggressive scrolls (#{no_change_count})...")
                        for i in range(10):
                            self.driver.execute_script(
                                'arguments[0].scrollTop = arguments[0].scrollHeight',
                                scrollable
                            )
                            time.sleep(0.8)
                        time.sleep(3)
            
            if scroll_count >= max_scrolls:
                print(f"\n⚠️ Mencapai batas maksimal scroll ({max_scrolls})")
                print(f"   Total ulasan yang dimuat: {total_reviews_before}")
                print(f"   Target: {target_reviews}")
                if total_reviews_before < target_reviews:
                    print(f"   ⚠️ Belum mencapai target! Mungkin perlu increase max_scrolls atau cek koneksi internet.")
                
        except Exception as e:
            print(f"❌ Error saat scroll: {e}")
            import traceback
            traceback.print_exc()
    
    def expand_all_reviews(self):
        """Klik semua tombol 'Selengkapnya' pada ulasan - dengan batch processing"""
        print(f"\n{'='*60}")
        print("🔍 EXPAND ULASAN PANJANG")
        print(f"{'='*60}\n")
        
        expanded_count = 0
        max_attempts = 8  # Lebih banyak attempt untuk 7000 ulasan
        
        for attempt in range(max_attempts):
            try:
                more_buttons = self.driver.find_elements(
                    By.XPATH,
                    '//button[@aria-label="Lihat ulasan lengkap" or @aria-label="See more" or contains(@class, "w8nwRe")]'
                )
                
                if not more_buttons:
                    if attempt == 0:
                        print("✅ Tidak ada tombol 'Selengkapnya' (semua ulasan sudah lengkap)")
                    break
                
                print(f"📝 Attempt {attempt + 1}: Menemukan {len(more_buttons)} tombol 'Selengkapnya'")
                
                # Process in batches
                batch_size = 50
                for batch_start in range(0, len(more_buttons), batch_size):
                    batch_end = min(batch_start + batch_size, len(more_buttons))
                    batch = more_buttons[batch_start:batch_end]
                    
                    print(f"   Processing batch {batch_start}-{batch_end}...")
                    
                    for idx, btn in enumerate(batch):
                        try:
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block: 'center'});",
                                btn
                            )
                            time.sleep(0.1)
                            
                            self.driver.execute_script("arguments[0].click();", btn)
                            expanded_count += 1
                            
                            if (expanded_count) % 100 == 0:
                                print(f"   Progress: {expanded_count} expanded")
                            
                            time.sleep(0.2)
                        except:
                            pass
                    
                    time.sleep(1)
                
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ Error expand reviews (attempt {attempt+1}): {e}")
        
        print(f"\n✅ Total {expanded_count} ulasan di-expand")
    
    def get_place_info(self):
        """Ambil informasi tempat"""
        info = {
            'nama_tempat': 'N/A',
            'rating_keseluruhan': 'N/A',
            'total_ulasan': 'N/A',
            'kategori': 'N/A'
        }
        
        try:
            time.sleep(2)
            
            try:
                info['nama_tempat'] = self.driver.find_element(
                    By.CSS_SELECTOR, 'h1.DUwDvf'
                ).text
            except:
                pass
            
            try:
                info['rating_keseluruhan'] = self.driver.find_element(
                    By.CSS_SELECTOR, 'div.F7nice span[aria-hidden="true"]'
                ).text
            except:
                pass
            
            try:
                total_text = self.driver.find_element(
                    By.CSS_SELECTOR, 'div.F7nice span span'
                ).text
                info['total_ulasan'] = total_text.replace('(', '').replace(')', '').strip()
            except:
                pass
            
            try:
                info['kategori'] = self.driver.find_element(
                    By.CSS_SELECTOR, 'button.DkEaL'
                ).text
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ Error getting place info: {e}")
        
        return info
    
    def scrape_all_reviews(self, url, max_scrolls=2000, target_reviews=7000):
        """
        Scrape SEMUA ulasan dari URL Google Maps
        
        Args:
            url: URL tempat Google Maps
            max_scrolls: Maksimal jumlah scroll (2000 untuk 7000+ ulasan)
            target_reviews: Target jumlah ulasan yang ingin di-scrape
        
        Returns:
            DataFrame berisi semua ulasan
        """
        print("🌐 Membuka URL...")
        self.driver.get(url)
        time.sleep(8)
        
        place_info = self.get_place_info()
        print(f"\n{'='*60}")
        print(f"📍 INFORMASI TEMPAT")
        print(f"{'='*60}")
        print(f"Nama: {place_info['nama_tempat']}")
        print(f"Rating: {place_info['rating_keseluruhan']}")
        print(f"Total Ulasan: {place_info['total_ulasan']}")
        print(f"Kategori: {place_info['kategori']}")
        print(f"Target Scrape: {target_reviews} ulasan")
        print(f"{'='*60}\n")
        
        try:
            print("🔍 Mencari dan membuka tab ulasan...")
            reviews_tab = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//button[contains(@aria-label, "Ulasan") or contains(@aria-label, "Reviews")]'
                ))
            )
            reviews_tab.click()
            print("✅ Tab ulasan dibuka")
            time.sleep(5)
        except TimeoutException:
            print("⚠️ Tab ulasan tidak ditemukan, mencoba scroll untuk mencari ulasan...")
            self.driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(3)
        
        try:
            print("🔄 Mengurutkan ulasan berdasarkan terbaru...")
            sort_button = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//button[@aria-label="Urutkan ulasan" or @aria-label="Sort reviews"]'
                ))
            )
            sort_button.click()
            time.sleep(2)
            
            newest_option = self.driver.find_element(
                By.XPATH,
                '//div[@role="menuitemradio" and contains(@data-index, "1")]'
            )
            newest_option.click()
            time.sleep(3)
            print("✅ Ulasan diurutkan berdasarkan terbaru")
        except:
            print("⚠️ Tidak bisa mengurutkan, lanjut scraping...")
        
        # Scroll untuk memuat SEMUA ulasan dengan target
        self.scroll_reviews_panel(max_scrolls, target_reviews)
        
        # Expand semua ulasan panjang
        self.expand_all_reviews()
        
        # Scrape data ulasan
        print(f"\n{'='*60}")
        print("📊 SCRAPING DATA ULASAN")
        print(f"{'='*60}\n")
        
        reviews_data = []
        
        try:
            time.sleep(2)
            
            review_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                'div.jftiEf'
            )
            
            total_found = len(review_elements)
            print(f"✅ Total ulasan ditemukan: {total_found}")
            
            if total_found == 0:
                print("\n❌ TIDAK ADA ULASAN DITEMUKAN!")
                print("Menyimpan debug files...")
                with open('debug_page_source.html', 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
                self.driver.save_screenshot('debug_screenshot.png')
                print("✅ Debug files disimpan")
                return pd.DataFrame()
            
            print(f"\n🔄 Memproses {total_found} ulasan...\n")
            start_time = time.time()
            
            for idx, review in enumerate(review_elements, 1):
                try:
                    review_dict = {
                        'no': idx,
                        'nama_tempat': place_info['nama_tempat'],
                        'nama_reviewer': 'N/A',
                        'rating': 'N/A',
                        'tanggal': 'N/A',
                        'ulasan': 'N/A',
                        'jumlah_ulasan_reviewer': 'N/A',
                        'foto': 'N/A'
                    }
                    
                    try:
                        review_dict['nama_reviewer'] = review.find_element(
                            By.CSS_SELECTOR, 'div.d4r55'
                        ).text
                    except:
                        pass
                    
                    try:
                        rating_elem = review.find_element(
                            By.CSS_SELECTOR, 'span.kvMYJc'
                        )
                        rating_text = rating_elem.get_attribute('aria-label')
                        review_dict['rating'] = rating_text.split()[0] if rating_text else 'N/A'
                    except:
                        pass
                    
                    try:
                        review_dict['tanggal'] = review.find_element(
                            By.CSS_SELECTOR, 'span.rsqaWe'
                        ).text
                    except:
                        pass
                    
                    try:
                        review_dict['ulasan'] = review.find_element(
                            By.CSS_SELECTOR, 'span.wiI7pd'
                        ).text
                    except:
                        try:
                            review_dict['ulasan'] = review.find_element(
                                By.CSS_SELECTOR, 'div.MyEned'
                            ).text
                        except:
                            pass
                    
                    try:
                        review_count = review.find_element(
                            By.CSS_SELECTOR, 'div.RfnDt span'
                        ).text
                        review_dict['jumlah_ulasan_reviewer'] = review_count.split()[0]
                    except:
                        pass
                    
                    try:
                        photos = review.find_elements(
                            By.CSS_SELECTOR, 'button[jsaction*="photo"]'
                        )
                        review_dict['foto'] = 'Ya' if len(photos) > 0 else 'Tidak'
                    except:
                        review_dict['foto'] = 'Tidak'
                    
                    reviews_data.append(review_dict)
                    
                    if idx % 100 == 0:
                        elapsed = time.time() - start_time
                        rate = idx / elapsed
                        remaining = (total_found - idx) / rate if rate > 0 else 0
                        print(f"⏳ Progress: {idx}/{total_found} ({(idx/total_found)*100:.1f}%) | Rate: {rate:.1f}/s | ETA: {remaining:.0f}s")
                    
                except Exception as e:
                    print(f"⚠️ Error scraping review #{idx}: {e}")
                    continue
            
            print(f"\n✅ Selesai memproses {len(reviews_data)} ulasan!")
            
        except Exception as e:
            print(f"❌ Error menemukan review elements: {e}")
            import traceback
            traceback.print_exc()
        
        return pd.DataFrame(reviews_data)
    
    def close(self):
        """Tutup browser"""
        self.driver.quit()


def main():
    """Fungsi utama untuk menjalankan scraper"""
    
    place_url = "https://www.google.com/maps/place/1009+Social+Space+-+Palagan/@-7.7291501,110.3815313,17z/data=!3m1!4b1!4m6!3m5!1s0x2e7a5970cc975d95:0x86b69a706d589f1!8m2!3d-7.7291501!4d110.3841062!16s%2Fg%2F11mdhkh6pl?entry=ttu&g_ep=EgoyMDI1MTIwOS4wIKXMDSoASAFQAw%3D%3D"
    
    print("="*60)
    print("🚀 GOOGLE MAPS REVIEW SCRAPER - ENHANCED")
    print("="*60)
    print("⚠️ CATATAN:")
    print("   - Target: 7000 ulasan")
    print("   - Proses bisa memakan waktu 30-60 menit")
    print("   - Jangan tutup atau minimize browser")
    print("   - Pastikan koneksi internet stabil")
    print("   - Biarkan script berjalan sampai selesai")
    print("="*60)
    
    scraper = GoogleMapsReviewScraper(headless=False)
    
    try:
        # Scrape dengan target 7000 ulasan
        df = scraper.scrape_all_reviews(
            place_url, 
            max_scrolls=3000,  # Increased untuk memastikan semua ulasan termuat
            target_reviews=7000
        )
        
        if len(df) > 0:
            print(f"\n{'='*60}")
            print(f"✅ BERHASIL!")
            print(f"{'='*60}")
            print(f"📊 Total ulasan: {len(df)}")
            print(f"📍 Tempat: {df['nama_tempat'].iloc[0]}")
            
            print(f"\n⭐ DISTRIBUSI RATING:")
            ratings = df['rating'].value_counts().sort_index(ascending=False)
            for rating, count in ratings.items():
                percentage = (count / len(df)) * 100
                bars = '█' * int(percentage / 2)
                print(f"   {rating} bintang: {count:4d} ulasan ({percentage:5.1f}%) {bars}")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            csv_file = f'google_maps_reviews_{timestamp}.csv'
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"\n💾 Data disimpan ke: {csv_file}")
            
            excel_file = f'google_maps_reviews_{timestamp}.xlsx'
            df.to_excel(excel_file, index=False, engine='openpyxl')
            print(f"💾 Data disimpan ke: {excel_file}")
            
            print(f"\n📋 PREVIEW 5 ULASAN PERTAMA:")
            print("="*60)
            for idx, row in df.head().iterrows():
                print(f"\n{idx+1}. {row['nama_reviewer']} - ⭐ {row['rating']}")
                print(f"   📅 {row['tanggal']}")
                ulasan_preview = row['ulasan'][:150] + "..." if len(row['ulasan']) > 150 else row['ulasan']
                print(f"   💬 {ulasan_preview}")
        else:
            print("\n❌ Tidak ada ulasan yang berhasil di-scrape!")
            print("Periksa file debug_page_source.html dan debug_screenshot.png")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print(f"\n{'='*60}")
        print("🔄 Menutup browser dalam 10 detik...")
        print("="*60)
        time.sleep(10)
        scraper.close()
        print("✅ Selesai!")


if __name__ == "__main__":
    main()