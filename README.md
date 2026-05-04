# Mini Store Console Application

Bu layihə, Python proqramlaşdırma dilində yazılmış, konsol (terminal) üzərindən işləyən sadə bir mağaza idarəetmə sistemidir. Layihədə istifadəçi girişi, məhsul kataloqu, səbət və alış-veriş prosesləri simulyasiya edilmişdir.

## 🚀 Xüsusiyyətlər

*   **Təhlükəsiz Giriş Sistemi:** 
    *   3 dəfə yanlış şifrə daxil edildikdə hesabın 10 saniyəlik bloklanması.
    *   İstifadəçi fəaliyyətlərinin log fayllarında (`history_username.log`) qeyd edilməsi.
*   **Məhsul İdarəetməsi:** 
    *   Kateqoriyalar üzrə (Geyim, Elektronika) məhsulların listələnməsi.
    *   Məhsul ID-si və miqdarına əsasən seçim imkanı.
*   **Səbət və Ödəniş:** 
    *   Məhsulların səbətə əlavə edilməsi.
    *   İstifadəçi balansına uyğun olaraq alış-verişin tamamlanması.
*   **Məlumatların Saxlanılması:** 
    *   İstifadəçilər, məhsullar, səbətlər və keçmiş alış-verişlər JSON formatında fayllarda saxlanılır.
*   **İstifadəçi Parametrləri:** 
    *   Şifrə dəyişdirmə imkanı.

## 🛠 Texnologiyalar

*   **Dil:** Python 3.x
*   **Məlumat Bazası:** JSON faylları (`json` modulu)
*   **Loglama:** Mətn əsaslı log faylları (`datetime` modulu)

## 📖 Necə İstifadə Etməli?

1.  Layihə fayllarını kompüterinizə yükləyin.
2.  Terminalda proqramı başladın:
    ```bash
    python main.py
