#Ajanda


## bilgiler
* Yazarlar: Abel Passos, Ângelo Abrantes ve Rui Fontes
* Güncelleme: 30 Mayıs 2023
* [Kararlı sürümü indirin][1]
* Uyumluluk: NVDA sürüm 2019.3 ve sonrası

<br>
## Sunum
Bu eklenti, randevuları ve etkinlikleri alarmlı veya alarmsız yazmanıza olanak tanır.  
İki farklı ajanda kullanabilirsiniz.  
Bunlar arasında geçiş yapmak için NVDA menüsü, Tercihler, Ayarlar, ajanda bölümüne gidin ve açılan kutudan kullanmak istediğiniz ajandayı seçin.  
İkinci satır boşsa, ikinci bir ajanda oluşturmak için \"Bir dizin seçin veya ekleyin\" düğmesini kullanın.  
Bu düğmeyi bir yol seçiliyken kullanırsanız, ajanda yoksa, ajanda yeni yola taşınır. Olursa, yalnızca yol değiştirilir ve kullanılan yeni yol ile her iki ajanda da korunur.  
NVDA her başlatıldığında, bu gün ve sonraki gün için randevular size hatırlatılacaktır. Bu hatırlatıcı, tüm randevuların listesini içeren bir pencere veya alarmı ayarlanmış randevular için diyalog ve sesli alarm içeren bir hatırlatıcı olabilir.  
Bu seçenek, eklentinin ayarlarından yapılandırılabilir.

<br>
## Komut
Eklentiyi çağırma komutu NVDA+F4'tür.  
Bunu, Girdi hareketleri iletişim kutusunda Ajanda başlığını genişleterek değiştirebilirsiniz.

<br>
## Nasıl çalışır:
* NVDA ekran okuyucusunu açtığınızda, bu günün randevuları görüntülenecektir.
* Ana pencerede tarihin değiştirileceği alanlar, seçilen tarih için randevular ve daha sonra anlatılacak olan bazı program kontrol butonları bulunmaktadır.  
Tarih alanları Yukarı/aşağı ok tuşlarıkullanılarak veya istenilen değer yazılarak değiştirilebilir. Tarih değiştirilirken günün randevuları otomatik olarak görüntülenecektir.

<br>
### Ana pencere için kısayol tuşları:
* Alt + 1-9: Basılan değere bağlı olarak gün sayısını değiştirir;
* Alt+0: Geçerli tarihe döner;
* Alt+sol ok: Önceki güne gider;
* Alt+sağ ok: Sonraki güne gider;
* Alt+Yukarı Ok: Bir hafta sonrasına gider;
* Alt+Aşağı ok: Bir hafta öncesine gider;
* Alt+Sayfa yukarı: Bir ay sonrasına gider;
* Alt+Sayfa aşağı: Bir ay öncesine gider;
* Enter: Bir randevu seçilirse düzenleme penceresini açar. Eğer randevu yoksa, yenisini oluşturmak için ilgili pencereyi açar.;
* Sil: Seçilen kaydı siler. Kaldır düğmesiyle aynı işlev;
* Control+f: "Ara" penceresini açar. "Ara" düğmesiile aynı işlevi görür;

<br>
### Ana penceredeki düğmelerin işlevleri ve ilgili kısa yol tuşları:
* Ekle (Alt+E): Seçilen tarihteki randevuları kaydetmek için bir pencere açar;
* Düzenle (Alt+D): Seçilen randevuyu düzenlemek için bir pencere açar;
* Kaldır (Alt+K): Seçilen randevuyu siler;
* Ara (Alt+A): Ajandada bilgi aramak için bir pencere açar;
* Çık (Alt+Ç): Pencereyi kapatır.

<br>
### Ekleme ve düzenleme işlevleri oldukça benzerdir ve bu nedenle anlatılacak pencere her iki işlevi de yerine getirir.
Temel fark, düzenleme yapabilmek için daha önce değiştirilecek bir randevu seçmiş olmanız gerektiğidir.  
Ayrıca, Düzenle işlevinde, seçilen randevu verileri değişiklik için pencerede görüntülenir. Ekle penceresinde ise, seçilen tarih haricindeki bilgi alanları boş olarak gelir.  

<br>
### Ekle ve Düzenle pencere alanları:
* gün/ay/yıl: Yukarı ile aşağı oklarla veya istenilen değer yazılarak değiştirilebilen tarih alanları
* saat/dakika: Aşağı ile yukarı ok tuşlarıyla veya istenilen değer yazılarak değiştirilebilen zaman alanları
* Açıklama: Randevu ile ilgili bilgilerin doldurulacağı alan;
* Alarmlar: Gerektiğinde işaretlenmesi gereken onay kutuları. Varsayılan olarak, randevu tarihi ve saatinden önce herhangi bir alarm seçildiğinde, tam saat alarmı otomatik olarak devreye girer.
* Tamam düğmesi (Alt+T): randevu bilgilerini takvime ekler
* İptal düğmesi (Alt+L): Girilen bilgileri kaydetmeden pencereyi kapatır.
* Ekle/Düzenle penceresinde, doldurulmuş bilgileri kaydetmek için Ctrl+Enter kısayolu bulunur. Bu, Tamam düğmesiyle aynı işlevi görür.

<br>
### Arama penceresi alanları:
* Arama türü: aşağıdaki seçeneklerden birini seçmelisiniz:
<br>
	* Metne göre ara: aramak istediğiniz şeyi yazmanız için bir düzenleme alanı açılacaktır. Tüm ifadeyi yazmak gerekli değildir, arama kelimelerin bölümleriyle yapılabilir;
	* Sonraki 7 gün: geçerli gün hariç, sonraki 7 gün için randevuları görüntüler;
	* Sonraki 30 gün: geçerli gün hariç, sonraki 30 gün için randevuları görüntüler;
	* Tarih aralığı: arama için başlangıç ​​ve bitiş tarihi alanlarını görüntüler;
<br>
* Ara düğmesi (Alt+A): Belirtilen kriterlere göre aramayı başlatır ve varsa sonuçları listeler.
* Ekle düğmesi (Alt+E): Ana penceredekiyle aynı ekleme işlevi. Aradaki fark, bir randevu seçtiyseniz, ekleme penceresi seçilen randevunun tarihinde olacaktır. Herhangi bir randevu seçilmemişse, geçerli tarih penceresini görüntüler;
* Düzenle düğmesi (Alt+D): Ana pencerede ki ile aynı düzenleme işlevdir. Düzenleme yapabilmek için bir randevunun seçili olması gerekir.
* Kaldır düğmesi (Alt+K): Seçili randevuyu Siler;
* Tümünü kaldır (Alt+T): Görüntülenen tüm randevuları siler;
* İptal düğmesi (Alt+L): arama penceresini kapatır ve ana pencereye döner.

[1]: https://github.com/ruifontes/agenda-for-NVDA/releases/download/2023.05.30/agenda-2023.05.30.nvda-addon