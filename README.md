### Yüz Tanıma Sistemi

Bu proje, bir yüz tanıma sistemi oluşturmayı ve bunu web tabanlı bir arayüzle kullanıcıya sunmayı hedeflemektedir. Kamera ile yüz verilerini toplar, bu verilerle bir model eğitir ve bu modeli kullanarak gerçek zamanlı yüz tanıma işlemleri gerçekleştirir. Sistem, OpenCV kütüphanesi ve Flask web framework'ü kullanılarak geliştirilmiştir.

## İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Özellikler](#özellikler)
- [Kullanım Alanları](#kullanım-alanları)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Kullanım Kılavuzu](#kullanım-kılavuzu)
  - [Yüz Verisi Toplama](#yüz-verisi-toplama)
  - [Model Eğitimi](#model-eğitimi)
  - [Gerçek Zamanlı Yüz Tanıma](#gerçek-zamanlı-yüz-tanıma)
  - [Loglar ve İzleme](#loglar-ve-izleme)
  - [Web Arayüzü Butonları](#web-arayüzü-butonları)
- [Proje Mimarisi](#proje-mimarisi)
  - [Dosya ve Klasör Yapısı](#dosya-ve-klasör-yapısı)
  - [Teknik Detaylar](#teknik-detaylar)
- [Potansiyel Geliştirmeler](#potansiyel-geliştirmeler)
- [Sıkça Sorulan Sorular](#sıkça-sorulan-sorular)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

## Proje Hakkında

Bu proje, yüz tanıma teknolojilerini öğrenmek ve uygulamak isteyenler için tasarlanmıştır. Proje, kamera aracılığıyla yüz görüntüleri toplar, bu görüntüleri kullanarak bir yüz tanıma modeli eğitir ve ardından bu modeli kullanarak tanıma işlemleri gerçekleştirir. Flask tabanlı bir web arayüzü, kullanıcının yüz verisi toplama, model eğitimi ve yüz tanıma işlemlerini kolayca yönetmesini sağlar. Ayrıca sistem, yapılan işlemleri loglar ve bu logları web arayüzünden takip etmeyi mümkün kılar.

## Özellikler

- **Yüz Verisi Toplama:** Farklı açılardan (düz, sağ, sol, yukarı, aşağı) yüz görüntüleri toplar ve bu verileri saklar.
- **Model Eğitimi:** Toplanan yüz görüntüleriyle bir LBPH (Local Binary Patterns Histogram) modeli eğitir.
- **Gerçek Zamanlı Yüz Tanıma:** Eğitilen model ile kameradan alınan görüntülerdeki yüzleri tanır.
- **Web Arayüzü:** Kullanıcı dostu bir arayüz ile tüm işlemleri kolayca yönetmenizi sağlar.
- **Loglama:** Sistem, yapılan tüm işlemleri loglar ve bu logları web arayüzünden takip etmeye olanak tanır.

## Kullanım Alanları

Bu proje, aşağıdaki gibi çeşitli uygulama alanlarında kullanılabilir:

- **Güvenlik Sistemleri:** Yetkisiz kişilerin erişimini engellemek için yüz tanıma kullanılabilir.
- **Kişisel Projeler:** Yüz tanıma teknolojilerini öğrenmek ve kişisel projelerde kullanmak isteyenler için idealdir.
- **Geliştirici Eğitimleri:** Yüz tanıma ve makine öğrenimi alanında eğitim almak isteyen geliştiriciler için bir öğrenme aracı olarak kullanılabilir.

## Gereksinimler

Proje, aşağıdaki yazılım ve kütüphaneleri gerektirir:

- Python 3.x
- Flask
- Flask-SocketIO
- OpenCV
- NumPy
- Pillow

Gerekli Python kütüphanelerini yüklemek için `requirements.txt` dosyasını kullanabilirsiniz:

```bash
pip install -r requirements.txt
```

## Kurulum

1. Projeyi GitHub'dan klonlayın:

   ```bash
   git clone https://github.com/vahap-18/python-yuz-tanima.git
   cd yuz-tanima-sistemi
   ```

2. Gerekli Python bağımlılıklarını yükleyin:

   ```bash
   pip install -r requirements.txt
   ```

3. Flask uygulamasını başlatın:

   ```bash
   python app.py
   ```

4. Tarayıcınız otomatik olarak açılacak ve uygulamayı `http://127.0.0.1:5000/` adresinde kullanabileceksiniz.

## Kullanım Kılavuzu

### Yüz Verisi Toplama

**1. Kullanıcı Adı Ekleme:**

Web arayüzünden yüz verisi toplamak istediğinizde, ilgili kişinin adını girmeniz gerekecektir. Ancak, bu adı girmeden önce, `app.py` dosyasındaki `names` dizisine bu adı eklemeniz gerekmektedir. `names` dizisi, tanınacak kullanıcıların isimlerini içeren bir listedir. Bu listeyi aşağıdaki gibi güncelleyebilirsiniz:

```python
names = ["mehmet", "vahap", "kadir", "deneme", "yeni_kullanici"]  # Yeni kullanıcı adını buraya ekleyin
```

**2. Veri Toplama:**

Web arayüzünde toplanacak yüz verileri için bir isim (kullanıcı adı) girin ve "Yüz Tanımayı Başlat" butonuna tıklayın. Sistem, sizden yüzünüzü farklı yönlere çeviriniz (düz, sağa, sola, yukarı, aşağı). Her açıdan 10 görüntü yakalanacaktır. Görüntüler yakalanırken web sutesi deki gömülü terminal ekranından gerçek zamanlı olarak izlenebilecektir. Bu görüntüler `data/` klasöründe, belirtilen isimle oluşturulan bir klasörde saklanır.

### Model Eğitimi

Yüz verilerini topladıktan sonra model eğitimi işlemini başlatmak için "Modeli Eğit" butonuna tıklayın. Sistem, toplanan yüz verileri ile bir LBPH (Local Binary Patterns Histogram) modeli eğitecek ve bu modeli `trainer/trainer.yml` dosyasına kaydedecektir.

### Gerçek Zamanlı Yüz Tanıma

Model eğitimi tamamlandıktan sonra eğitilmiş model, kameradan alınan görüntülerdeki yüzleri tanımak için kullanılır. Tanıma işlemini başlatmak için "Model Tanımayı Başlat" butonuna tıklayın. Tanıma işlemi sırasında, tanınan kişinin adı ve tanıma güven oranı kullanıcıya bildirilir. Güven oranı %60'ın üzerinde ise sistem, kişinin kimliğini doğrular ve bir kapı açılmış gibi bir bildirim verir.

### Loglar ve İzleme

Sistem, yapılan tüm işlemleri `log.txt` dosyasına kaydeder. Web arayüzünden "Loglar" sekmesine giderek bu işlemleri takip edebilirsiniz. Tanıma işlemi, veri toplama ve model eğitimi süreçlerinde gerçekleşen her türlü etkinlik burada listelenir.

### Web Arayüzü Butonları

- **Yüz Tanımayı Başlat:** Bu buton, yüz verisi toplama işlemini başlatır. Kullanıcı adını girdikten sonra bu butona basarak yüz verilerini toplayabilirsiniz.
- **Modeli Eğit:** Bu buton, toplanan verilerle yüz tanıma modelini eğitir. Eğitilen model `trainer/trainer.yml` dosyasına kaydedilir.
- **Model Tanımayı Başlat:** Bu buton, kameradan gelen görüntülerdeki yüzleri tanımak için eğitilen modeli kullanır. Tanıma işlemi başlatıldıktan sonra, tanınan kişilerin isimleri ve güven oranları loglanır.
- **Logları Göster:** Bu buton, sistemde yapılan tüm işlemlerin loglarını görüntüler. İşlemleri gerçek zamanlı olarak takip edebilirsiniz.

## Proje Mimarisi

### Dosya ve Klasör Yapısı

- **app.py:** Flask uygulamasının ana dosyasıdır. Web arayüzü ve API işlemleri burada tanımlanır.
- **veri_toplama.py:** Yüz verisi toplama işlemlerini gerçekleştiren modüldür.
- **veri_ogrenme.py:** Toplanan yüz verileri ile modeli eğiten modüldür.
- **tanyıcı.py:** Eğitilmiş modeli kullanarak yüz tanıma işlemlerini gerçekleştiren modüldür.
- **templates/index.html:** Web arayüzü için HTML şablonu.
- **static/**: Web arayüzünde kullanılan statik dosyalar (CSS, JavaScript vb.).
- **data/**: Toplanan yüz verilerinin saklandığı klasör. Her kişi için bir klasör oluşturulur.
- **trainer/**: Eğitilmiş modelin saklandığı klasör.
- **log.txt:** Log kayıtlarının saklandığı dosya.
- **Cascade/**: Yüz algılama için kullanılan Haarcascade XML dosyaları.

### Teknik Detaylar

#### Veri Toplama

Sistem, kullanıcının yüz görüntülerini kamera aracılığıyla toplar. Yüz algılama, OpenCV'nin Haarcascades yöntemi ile gerçekleştirilir. Her bir görüntü, belirli bir boyuta ölçeklendirilir ve `data/` klasöründe, kullanıcının adıyla oluşturulan bir klasörde saklanır. Toplama işlemi sırasında, kullanıcıdan yüzünü farklı yönlere çevirmesi istenir. Bu, modelin çeşitli açılardan veri toplayarak daha sağlam bir eğitim almasını sağlar.

#### Model Eğitimi

Model eğitimi, LBPH (Local Binary Patterns Histogram) algoritması kullanılarak yapılır. LBPH, düşük çözünürlüklü görüntülerde etkili bir performans sağlar ve yüz tanıma uygulamaları için yeterli bir doğruluk sunar. Eğitim süreci, toplanan yüz görüntülerini analiz ederek model parametrelerini optimize eder. Eğitilmiş model `trainer/trainer.yml` dosyasına kaydedilir ve bu dosya, gerçek zamanlı tanıma işlemleri için kullanılır.

#### Gerçek Zamanlı Tanıma

Gerçek zamanlı yüz tanıma, eğitimli LBPH modelini kullanarak yapılır. Kamera görüntüleri sürekli olarak analiz edilir ve tanımlanan yüzler, daha önce eğitilmiş modeldeki yüzlerle karşılaştırılır. Yüz tanıma süreci, gerçek zamanlı olarak gerçekleşir ve tanınan kişinin adı ile güven oranı ekranda görüntülenir. Güven oranı %60'ın üzerinde ise sistem, tanınan kişinin kimliğini doğrular.

#### Web Arayüzü

Flask kullanılarak geliştirilen web arayüzü, kullanıcının yüz verilerini toplamasına, modeli eğitmesine ve yüz tanıma işlemlerini başlatmasına olanak tanır. Flask-SocketIO, arka planda gerçekleşen işlemleri (yüz tanıma, model eğitimi vb.) gerçek zamanlı olarak kullanıcıya aktarır. Arayüzdeki butonlar, kullanıcı etkileşimlerini yönetir ve işlemleri başlatır.

## Potansiyel Geliştirmeler

- **Veri Artırımı:** Mevcut veri setini genişletmek ve artırmak için veri artırma teknikleri kullanılabilir. Bu, modelin doğruluğunu ve genelleme yeteneğini artırabilir.
- **Derin Öğrenme Modelleri:** LBPH yerine, daha karmaşık derin öğrenme modelleri (örneğin, CNN – Convolutional Neural Networks) kullanılarak tanıma doğruluğu artırılabilir.
- **Kullanıcı Arayüzü İyileştirmeleri:** Web arayüzü daha kullanıcı dostu hale getirilebilir, örneğin, daha gelişmiş görselleştirme araçları ve daha sezgisel bir kullanıcı deneyimi sunulabilir.
- **Performans İyileştirmeleri:** Tanıma ve eğitim süreçlerinin hızını artırmak için optimizasyon teknikleri ve daha hızlı algoritmalar kullanılabilir.

**NOT:** Proje geliştirilmesi devam edecektir.

## Sıkça Sorulan Sorular

**S: Yüz verilerini toplarken nelere dikkat etmeliyim?**

**C:** Yüz verilerini toplarken, farklı açılardan ve iyi aydınlatılmış bir ortamda yüzünüzün fotoğraflarını çekmeye özen gösterin. Ayrıca, çeşitli ifadeler ve yüz pozisyonları kullanarak veri toplamak modelin doğruluğunu artırır.

**S: Model eğitim süreci ne kadar sürer?**

**C:** Model eğitimi süresi, toplanan veri miktarına ve bilgisayarın işlem gücüne bağlı olarak değişir. Genellikle, küçük veri setleri için eğitim birkaç dakika sürebilir, ancak büyük veri setleri için bu süre uzayabilir.

**S: Gerçek zamanlı yüz tanıma nasıl çalışır?**

**C:** Gerçek zamanlı yüz tanıma, kamera görüntülerindeki yüzleri sürekli olarak analiz eder. Eğitilmiş model ile bu yüzler karşılaştırılır ve tanımlanır. Tanıma işlemi anında gerçekleştirilir ve sonuçlar kullanıcıya bildirilir.

**S: Verilerim güvende mi?**

**C:** Toplanan yüz verileri ve model dosyaları, proje dizinindeki uygun klasörlerde saklanır. Veri güvenliği için, dosyaların erişim izinlerini düzenleyebilir ve yetkisiz erişimi engellemek için gerekli önlemleri alabilirsiniz.

## Katkıda Bulunma

Katkıda bulunmak isteyenler, aşağıdaki adımları takip edebilir:

1. Projeyi fork edin.
2. Yeni bir branch oluşturun (`git checkout -b feature/yenilik`).
3. Yapmak istediğiniz değişiklikleri yapın ve commit edin (`git commit -am 'Yeni özellik ekle'`).
4. Değişikliklerinizi push edin (`git push origin feature/yenilik`).
5. Bir pull request oluşturun.

Her türlü katkı için teşekkür ederiz!

## Lisans

Bu proje [MIT Lisansı](https://opensource.org/licenses/MIT) altında lisanslanmıştır.
