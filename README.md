# AKILLI TRADE AI — başlangıç prototipi

Bu paket, bilgisayarda yerel olarak çalıştırılan bir **demo / sanal işlem** prototipidir.
Gerçek emir göndermez, Binance TR veya Midas hesabına bağlanmaz ve ekrandaki fiyatlar örnek veridir.

## Gereksinimler
- Python 3.10 veya üzeri

## Kurulum
1. ZIP'i çıkarın.
2. Klasör içinde terminal/komut istemi açın.
3. `python -m venv .venv` çalıştırın.
4. Windows: `.venv\\Scripts\\activate`
   macOS/Linux: `source .venv/bin/activate`
5. `pip install -r requirements.txt`
6. `uvicorn app:app --reload`
7. Tarayıcıda `http://127.0.0.1:8000` adresini açın.

## Şu an çalışanlar
- 7.500 TL sanal bakiye
- Demo varlık fiyatları
- Sanal AL / SAT emirleri
- Sanal portföy ve işlem geçmişi
- Basit demo sinyalleri

## Henüz yapılmayanlar
- Binance TR canlı veri ve emir entegrasyonu
- Midas Menkul canlı veri / emir entegrasyonu
- Haber sağlayıcısı ve haber duygu analizi
- Güvenilir geriye dönük test ve strateji doğrulaması

## Güvenlik / canlıya geçiş
API anahtarı veya gizli anahtarı kaynak koda yazmayın, sohbet üzerinden paylaşmayın.
Gerçek işlem entegrasyonu eklenirse önce yalnızca okuma izniyle başlanmalı; para çekme izni hiçbir zaman verilmemeli.
Canlı emir özelliği varsayılan olarak kapalı kalmalı ve ayrı bir açık onay gerektirmelidir.

Midas Menkul'ün bireysel müşterilere sunduğu resmi API erişimi ve kullanım şartları doğrulanmadan otomasyon bağlantısı eklenmeyecektir.


## Telefona ana ekran uygulaması olarak yükleme (PWA)
Bu sürüm PWA manifesti ve service worker içerir. Ana ekrana yükleme için uygulamanın HTTPS üzerinden yayınlanması gerekir (localhost geliştirme için istisnadır).
1. Uygulamayı HTTPS destekleyen bir sunucuya dağıtın.
2. Android Chrome'da uygulama adresini açın.
3. Tarayıcı menüsünden **Uygulamayı yükle** veya **Ana ekrana ekle** seçeneğine dokunun.
4. Uygulama simgesi telefon ana ekranında görünür.

Not: PWA ön yüzü telefona yüklenebilir; API sunucusu yine çalışır durumda olmalıdır. İnternet yokken yalnızca önceden önbelleğe alınmış arayüz açılır; fiyatlar ve emir API'si çevrimdışı çalışmaz.
