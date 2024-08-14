import tkinter as tk #tkinter kütüphanesini kısaltarak tk denildi.
import random
from PIL import Image, ImageTk


root = tk.Tk() # tk kütüphanesindeki Tk sınıfını kullanarak root adlı pencere oluşturuldu.
root.title("Snake Game") #Pencereye Snake Game ismi verildi.

global dolum_kismi , after_id
direction = 'right'
after_id = None
skor = 0


xx = (root.winfo_screenwidth() / 2) - (675 / 2) #root.winfo_screenwidth() ekranın genişliğini verir.(675 / 2) pencerenin yarı değerini verir. Rootun sol üst köşesi.
                                                #Böylece xx'in pencerenin ortadan ne kadar uzakta olduğu hesaplanır.
yy = (root.winfo_screenheight() / 2) - (500 / 2) #Sağ alt köşesi


root.geometry(f"{675}x{500}+{int(xx)}+{int(yy)}") #Rootun 675x500 piksel boyutunda ve sırasıyla x1 y1 ve x2 y2 koordinatları
root.resizable(False, False) #Sırasıyla pencere genişliği ve yüksekliği boyutlandırılamayacak şekilde ayarlandı.


canvas = tk.Canvas(root, bg='lightgreen', width=400, height=500) # tk kütüphanesindeki kullanılarak Canvas sınıfı kullanılarak canvas adlı bir widget oluşturuldu.
#root üstüne eklenildiği için root parametresi eklendi , arka rengi bg kullanılarak açık yeşil yapıldı ve yatayda 400 dikeyde 500 pksel olarak ayarlandı.
canvas.place(relx=0.0, rely=0.0) #canvasın yeri belirlendi.

canvas2 = tk.Canvas(root, bg='gray', width=270,height=500) #Rootun sağ tarafına canvas2 adlı yeni bir canvas eklendi.
canvas2.place(relx=1 ,rely=0.5,anchor='e') # canvas2'nin yeri belirlendi ve anchor=e kullanılarak sağ merkeze sabitlendi.

uygulama_bari1_label = tk.Label(root, text="Level 1", bg='purple', fg='white', width=5, height=1) #Uygulama barı kısmı ilk açıldığında level1 yazacak mor renkte görünecek şeklinde tanımlandı.
uygulama_bari1_label.place(x=580, y=125)  

ilerleme_bari1 = tk.Canvas(root, width=150, height=17, bg='lightgrey') #Yenilen yiyeceklere göre ilerleyen bir bar oluşturuldu.
ilerleme_bari1.place(x= 420, y=125) #place kullanılarak x ve y eksenine göre yeri belirlendi.

dolum_kismi = ilerleme_bari1.create_rectangle(0,0,0,15, fill='purple') # Barın içinde dolan kısım için create_rectangle oluşturularak dikdörtgen şekli verildi. Fill ile de açık gri oldu.


dikey_bar = canvas2.create_rectangle(237, 203, 242, 280, fill='white',outline='lightgray') #İlk levelda sokak direğinden gecekonduya ilerlemeyi göstermek için oluşturulan bar.
ikon_bari = canvas2.create_rectangle(50, 275, 220, 280, fill='white',outline='lightgray')  # 2. levelda gecekondu ile ev arasındaki ilerlemeyi gösteren bar.
dikey_bar2 = canvas2.create_rectangle(35, 302, 40, 430, fill='white',outline='lightgray')  # 3. levelda ev ile saray arasındaki ilerlemeyi gösteren bar.
#Canvas2'nin üstüne çizildiği ve dikdörtgen şeklinde çizildiği için canvas.create kullanıldı. Fill ile iç kısmı otuline ile çevresi renklendirildi. 

bar = 0
yenilen_yiyecek = 0
yenilen_yiyecekk=0
yenilen_yiyecekkk=0


def dikey_bar_doldurma(): #Oluşturulan dikey_barın kullanılması için oluşturulan fonksiyon
    global dikey_bar , o_anki_skor
    
    max_steps = 5 #Bar beş adımda bitecek 
    canvas2_height = 59 #dikey barın uzunluğu değişkene aktarıldı.
    y=(canvas2_height / max_steps) * o_anki_skor #Mat. işlem yapılarak her yenilen yiyecekte ne kadar ilerleneceği y değişkenine aktarıldı.

    while o_anki_skor<=5: #o_anki_skor 5'ten küçük eşitken çalış.

        canvas2.create_rectangle( #Dikdörtgen zemin oluşturuldu.
            237, 203, #Üst sol köşe
            242, 280, #Alt sağ köşe
            fill='purple', outline='lightgray' #Zemin mor , kenarları ise açık gri renk
        )

        canvas2.create_rectangle( #Yiyecek yenildğinde oluşan  kısım.
            237, 203 + y,  # Üst sol köşe. +y yapılarak barın yukarıdan aşağıya doğru doldurulması sağlandı.
            242, 280,     # Alt sağ köşe
            fill='white', outline='lightgray'  #İç kısım beyaz kenarlar ise açık gri.
        )
        break #o_anki_skor 5'ten büyük olunca döngüden çık.

    canvas2.update() #Değişikliklerin ekrana yansıması için update yaptık.



def ikon_bari_doldurma(): #İkon_barının kullanılması için oluşturulan fonksiyon.
    global yenilen_yiyecekk , ikon_bari

    yenilen_yiyecekk = o_anki_skor-5 
    while 5<o_anki_skor<=15:      
        max_steps = 10 #Toplam adım sayısı 10.
        canvas2_width = 170 #İkon_barının uzunluğu 170 piksel
        y=(canvas2_width / max_steps) * yenilen_yiyecekk #Her yiyecek yenildiğinde barın ne dar ilerleyeceğinni gösteren işlem.

        canvas2.create_rectangle( #Barın beyaz zemini
            50, 275,  # Üst sol köşe
            220 , 280 ,  # Alt sağ köşe
            fill='blue', outline='lightgray'  # Zemin mavi ve kenar çizgisi açık gri
        )

        canvas2.create_rectangle( # Dolu kısmı oluştur
            50, 275,   # Üst sol köşe
            220-y , 280 ,  # Alt sağ köşe. -y yapılarak sağdan sola barın doldurulması sağlandı.
            fill='white', outline='white'  #İç kısmı ve çevresi beyaz.
        )

        canvas2.update() #Değişimin yansıması için update edildi.
        break

   
def dikey_bar2_doldurma(): #Dikey_bar2'nin kullanılması için oluşturulan fonksiyon.
    global dikey_bar2 , yenilen_yiyecekkk
    
    yenilen_yiyecekkk = o_anki_skor-15  
    max_steps = 15 #Toplam adım sayısı
    canvas2_height = 130 #barın uzunluğu
    y=(canvas2_height / max_steps) * yenilen_yiyecekkk #Her yeniilen yiyecekle birlikte dikey_bar2'nin ne kadar ilerleyeceği

    while 15<o_anki_skor<=30:
        canvas2.create_rectangle(     # Beyaz zemin oluşturuldu
            35, 302, #Üst sol köşe
            40, 430, #Alt sağ köşe
            fill='yellow', outline='lightgray'  # Zemin beyaz ve kenar çizgisi açık gri
        )

        # Dolu kısmı oluştur
        canvas2.create_rectangle(
            35, 302+y,  #Üst sol köşe. +y yapılarak aşağı doğru barın dolması sağlandı.
            40, 430,    # Alt sağ köşe
            fill='white', outline='white'  # İçi , çerçevesi beyaz
        )
        break

    canvas2.update() #Canvasta olan değişimleri güncellem için yazıldı.


def uygulama_bari1(): # 30 yenilen yiyecekte sınırsız level olması için oluşturulan fonksiyon
    global yenilen_yiyecek , bar , renkler 
    global o_anki_skor,renkler,seviye,dolum_kismi    

    yeni_seviye = seviye
    renk = renkler[yeni_seviye % len(renkler)-1] #renklerin hangi sıralamada verileceği belirlendi
    renk2 = renkler2[(yeni_seviye % len(renkler))-1] #Oyun arka plan renginin değişim sıralaması  


    if yenilen_yiyecek<=5: #Eğer yenilen yiyecek sayısı 5'e küçük eşitse
                seviye=1 #Seviye yani level 1 olsun.
                uygulama_bari1_label = tk.Label(root,text=f'Level: {seviye}',bg='purple',fg='white',width=5,height=1)
                uygulama_bari1_label.place(x=580,y=125)    #Labelda text olarak Level 1 yazar. Rengi mor , büyüklüğü yatayda 5 dikeyde ise 1 olur.            
                bar = 0 
                ilerleme_bari1.delete('all')    #Bar önceden doluysa sıfırlanır.     
                bar =(o_anki_skor/5)*150        #Her yenilen yiyecek miktarına göre barın ilerleme miktarı ayarlanır.
                dolum_kismi = ilerleme_bari1.create_rectangle(0,0,0,15, fill='purple') #Dolum kısmının ilk hali
                ilerleme_bari1.coords(dolum_kismi, (0, 0, bar, 15)) #Her ilerlemede ilerleme barının nasıl ilerleyeceği
                canvas.config(bg='light green') #Level 1'de canvasın arka plan rengi

                if bar > 150: #Eğer barın doluluğu 150'yi geçerse 150'yi geçme.
                    bar = 150
   
    elif 5< yenilen_yiyecek<=15: #Eğer yenilen yiyecek sayısı 5 ile 15 arasındaysa 
                seviye=2         #Seviye yani level 2 olsun.      
                uygulama_bari1_label = tk.Label(root,text=f'Level: {seviye}',bg='blue',fg='white',width=5,height=1)
                uygulama_bari1_label.place(x=580,y=125)     #Labelda text olarak Level 2 yazar. Rengi mavi , büyüklüğü yatayda 5 dikeyde ise 1 olur.     
                bar = 0 
                ilerleme_bari1.delete('all')     #Bar önceden doluysa sıfırlanır.       
                bar =((yenilen_yiyecek-5)/10)*150 #Her yenilen yiyecek miktarına göre barın ilerleme miktarı ayarlanır.
                dolum_kismi = ilerleme_bari1.create_rectangle(0,0,bar,15,fill='blue') #Dolum kısmının ilk hali
                ilerleme_bari1.coords(dolum_kismi, (0, 0, bar, 15))  #Her ilerlemede ilerleme barının nasıl ilerleyeceği
                canvas.config(bg='powder blue') #Level 2'de canvasın arka plan rengi
   
    elif 15<yenilen_yiyecek<=30: #Eğer yenilen yiyecek sayısı 15 ile 30 arasındaysa 
                seviye=3         #Seviye yani level 3 olsun.  
                uygulama_bari1_label = tk.Label(root,text=f'Level: {seviye}',bg='orange',fg='white',width=5,height=1)
                uygulama_bari1_label.place(x=580,y=125)    #Labelda text olarak Level 3 yazar. Rengi turuncu , büyüklüğü yatayda 5 dikeyde ise 1 olur.            
                bar = 0 
                ilerleme_bari1.delete('all')   #Bar önceden doluysa sıfırlanır. 
                bar =((yenilen_yiyecek-15)/15)*150  #Her yenilen yiyecek miktarına göre barın ilerleme miktarı ayarlanır.
                dolum_kismi = ilerleme_bari1.create_rectangle(0,0,bar,15,fill='orange')
                ilerleme_bari1.coords(dolum_kismi, (0, 0, bar, 15))
                canvas.config(bg='lightyellow') #Level 3'de canvasın arka plan rengi
                


    elif yenilen_yiyecek>30 :  #Eğer yenilen yiyecek sayısı 30'dan büyükse arasındaysa  
        bar =0   
        ilerleme_bari1.delete('all')
        bar = ((yenilen_yiyecek-30) / 5) * 150 #Yenilen yiyecek miiktarı 30 dan büyük fakat bar 5 tane yiyecekle dolacağı için ona göre hesaplandı.
        dolum_kismi = ilerleme_bari1.create_rectangle(0, 0, bar, 15, fill=renk) #Dolum kısmının ilk hali ve her seviyede belirlenen renk fill ile gösterildi.
        ilerleme_bari1.coords(dolum_kismi, (0, 0, bar, 15)) #İlerleme barının dolum şekli
        canvas.config(bg=renk2) #Her levela göre canvas arka plan rengi renk2 listesine göre gösterildi.

        if bar >= 150 and yenilen_yiyecek ==35 : #Eğer barın doluluğu 150'yi geçerse 150'yi geçme.
             yenilen_yiyecek =30

    ilerleme_bari1.update()        
       

renkler = ["purple","blue","orange","red","green"] #İlerleme ve uygulama barının renklerin bulunduğu liste
renkler2 =['lightgreen','powder blue','light yellow','light blue','light goldenrod'] #Canvasın arka plan renkleri

def uygulama_bari():
    global o_anki_skor, yenilen_yiyecek, bar,seviye, renkler

    yenilen_yiyecek+=1
       
    if  o_anki_skor%5==1: #Eğer o anki skor 5'e bölündüğünde 1 kalıyorsa
                
                seviye = ((o_anki_skor-15) //5)+1 #Seviye 15'ten çıkarılmalı çünkü işleme göre 4 çıkmalı
                renk = renkler[(seviye % len(renkler))-1]   #uygulama ve ilerleme barına her seviyede farklı renk verildi     
                uygulama_bari1_label = tk.Label(root,text=f'Level: {seviye}',bg=renk,fg='white',width=5,height=1)
                uygulama_bari1_label.place(x=580,y=125)  #Labelda text olarak Level ve seviye o an neyse o yazar. Rengi listede bulunan sıradaki , büyüklüğü yatayda 5 dikeyde ise 1 olur. 
                dikey_bar_doldurma()
                ikon_bari_doldurma()
                dikey_bar2_doldurma()
                uygulama_bari1()       
                update()     
   

    else:

            uygulama_bari1()
            dikey_bar_doldurma()
            ikon_bari_doldurma()
            dikey_bar2_doldurma()

              

def update(): #seviye değişimini labelda gösterebilmek için oluşturduğumuz fonksiyon.
    global seviye
    uygulama_bari1_label.config(text=f"Level: {seviye}")

def resim_ve_label_olustur(ikon_yolu, boyut, arka_plan, x, y):
    """Belirtilen yol ve boyutla resmi yükler, uygun boyuta getirir ve bir Label oluşturur."""

    resim = Image.open(ikon_yolu) #resim dosyasını açar.
    resim = resim.resize(boyut) # resim dosyasını istenilen boyuta getirir.
    foto = ImageTk.PhotoImage(resim) # resmi tkintera uygun hale getirmek için yapıldı.
    label = tk.Label(root, image=foto, bg=arka_plan)
    label.image = foto  # Referansı saklamak için
    label.place(x=x, y=y) #resimlerin konumu
    #return label


# İkonları ve label'ları oluştur
kisi_satiri = tk.Label(root, bg='gold', height=1, width=7, text='Narin') #Kisinin isminin yazılı olduğu label.
kisi_satiri.place(x=605, y=71)#labelin konumu

#Sırasıyla resimlerin yolu , istenilen boyutları , arka plan renkleri ve bulundukları x ve y konumları
icon_label = resim_ve_label_olustur('C:/Users/guzel/Desktop/python/ikon/princess.png', (35,35), 'light blue', 615, 30)
kupa_label = resim_ve_label_olustur('C:/Users/guzel/Desktop/python/ikon/kupa1.png', (35,35), 'grey', 420, 30)
kare_label = resim_ve_label_olustur('C:/Users/guzel/Desktop/python/ikon/square.jpeg', (25,25), 'gray', 425, 75)
sokak_label = resim_ve_label_olustur('C:/Users/guzel/Desktop/python/ikon/sokak.png', (35,35), 'gray', 630, 160)
gecekondu_label = resim_ve_label_olustur('C:/Users/guzel/Desktop/python/ikon/gecekondu.png', (35,35), 'gray', 630, 255)
ev2_label = resim_ve_label_olustur('C:/Users/guzel/Desktop/python/ikon/ev2.png', (35,35), 'gray', 415, 255)
saray_label = resim_ve_label_olustur('C:/Users/guzel/Desktop/python/ikon/saray.png', (45,45), 'gray', 415, 440)

#Skorun yazılı olduğu kısım. Arka planı gri, oyun açılınca labelda yazan text ise 0. fontu ise belirlenen gibidir.
skor_label = tk.Label(root, bg='gray', text='0', font=('Helvetica', 14), width=2, height=1)
skor_label.place(x=460, y=77)


en_yuksek_skor = 0 # En yüksek skorun ilk durumu
en_yuksek_label = tk.Label(root, bg='gray', font=('Helvetica', 14), width=2, height=1) # En yğksek skor için oluşturulan label. Arka font rengi gri.
en_yuksek_label.place(x=462, y=35)
en_yuksek_label.config(text=f"{en_yuksek_skor}") #en yüksek skorun dinamik olarak değişimini günceller.

# Yılanın başlangıç kısmı
yilan = [] #Yılan büyüyeceği için ve bu sebeple parçalarını da ekleyebilmek için liste oluşturduk.
yilan.append(canvas.create_rectangle(15, 400, 30, 412, fill='green', outline='green')) #olusturlan yılanı append ile yılan listtesine ekler. Yeşil renk bir yılan oluşturuldu.
  

def random_color(): #Oluşturulan renklerin random renklerde olması için oluşturulan fonksiyon.
    r = random.randint(0, 255) #0-255 arasındakı rengidir.
    g = 0    #yılan yeşil renk olduğu için yeişl renk sıfırlandı.
    b = random.randint(0, 255) #0-255 arasındaki mavi renktir.
    return f"#{r:02x}{g:02x}{b:02x}" #rgb'yi birleştirerek rastgele hex sayılar üretir böylece rastgele renkler üretir


def yiyecek_olusturma(): #Rastgele yerlerde yiyecek oluşturmak için fonksiyon oluşturuldu.
    while True: 
        
        x = random.randint(0, (400 // 10 - 1)) * 10 #400 canvasın uzunluğunu 10'a bölerek belli alanlar oluşturuuldu. Her alana 10 piksellik yiyecek bırakıldı.
        y = random.randint(0, (500 // 10 - 1)) * 10 #500 canvasın uzunluğunu 10'a bölerek belli alanlar oluşturuuldu. Her alana 10 piksellik yiyecek bırakıldı.
        food_coords = (x, y, x + 10, y + 10) #Yiyeceğin koordinatları. x ve y sol üst , x+10 ve y+10 sağ alt koordinat. +10 ekkleyerek 10x10'luk yiyecekler oluşturuldu.

        yilan_coords = canvas.coords(yilan[0]) #Yılanın ilk baştaki koordinatlarınıalır ve liste halinde döndürür.
        yilan_koordinat = (yilan_coords[0], yilan_coords[1], yilan_coords[2], yilan_coords[3]) #Yılanın x1 , y1 , x2 ve y2 koordinatlarını tuple halinde döndürür.

         #Yiyeceğin herhnagi bir parçasının yılanın başına temas etmemesi sağlanır.
        if not (food_coords[0] <= yilan_koordinat[2] and food_coords[2] >= yilan_koordinat[0] and food_coords[1] <= yilan_koordinat[3] and food_coords[3] >= yilan_koordinat[1]):
            color = random_color() #oluşturulacak yiyecekler için rastgele renk bbelirlenir.
            return canvas.create_rectangle(x, y, x + 10, y + 10, fill=color ,outline=color ) #Eğer bir sorun oluşmazsa döngü sürdüğü müddetçe yiyecek oluşturur.
            


def yon_belirleme():
    global direction,after_id,bar
    
    # Son parça hariç tüm parçaların koordinatlarını güncelle
    for i in range(len(yilan) - 1, 0, -1): # yılan -1 yılanın son parçasının indisi. 0 ise 0' a kadar devam edeceği anlamını taşır. -1 ise sondan başa doğru anlamını taşır.
        coords = canvas.coords(yilan[i - 1]) #Bir önceki yılan parçasının koordinatlarını alır 
        canvas.coords(yilan[i], coords) #Alınan koordinatları yılanın şu anki yılana atar.

    coords = canvas.coords(yilan[0]) #Bu koordinatları alarak x1,y1,x2 ve y2 koordinatlarını belirler.
    x1, y1, x2, y2 = coords
    
    #Yılan hangi yöne doğru giderse belirlenen yılan koordinatları değiştirilir..
    if direction == 'up':
        new_coords = (x1, y1 - 10, x2, y2 - 10)
    elif direction == 'down':
        new_coords = (x1, y1 + 10, x2, y2 + 10)
    elif direction == 'right':
        new_coords = (x1 + 10, y1, x2 + 10, y2)
    elif direction == 'left':
        new_coords = (x1 - 10, y1, x2 - 10, y2)

    #Eğer yılan canvas kenarlarına çarparsa game over olur.
    if not (0 <= new_coords[0] < 400 and 0 <= new_coords[1] < 500 and 0 <= new_coords[2] <= 400 and 0 <= new_coords[3] <= 500):
        game_over()
        return 

    #Burda 1. nesne hareket ettirilmek istenen nesne(yılanın başı). 2. ve 3. ise ne x ve y ekseninde ne kadar hareket ettirileceği
    canvas.move(yilan[0], new_coords[0] - x1, new_coords[1] - y1)

    yiyecek_yeme() #Yılanın yeni pozisyonu belirlendikten sonra yeni yiyecek yiyip yemediğ kontrol edilir.
    kendini_yeme() #Yeni poziyondan sonra kendini yiyip yemediği kontrol edilir.
    after_id = root.after(95, yon_belirleme) #Yön belirleme çagrılınca 95 ms bekler bu da bizim hızımızı ayarlar.


def yon_degisimi(new_direction): 
    global direction,after_id
    #Hangi yöne giderse onun tersi yöne gidemez.
    if new_direction == 'up' and direction != 'down':
        direction = new_direction #Seçilen yön benim yeni yönüm
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction  
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'left' and direction != 'right':
        direction = new_direction

#Klavyedeki yön tuşlarını aktive eder.
#Lambda kısa fonksiyonları çalıştırmka için kullanılır. event ise burda kullanıcının klavye değişimini sağlar.
root.bind('<Up>', lambda event: yon_degisimi('up'))
root.bind('<Down>', lambda event: yon_degisimi('down'))
root.bind('<Left>', lambda event: yon_degisimi('left'))
root.bind('<Right>', lambda event: yon_degisimi('right'))



def yiyecek_yeme():
    #Yiyecek yenildiğnde oluşan değişimler burada oluşturulur.
    global food , yenilen_yiyecek

    yilan_coords = canvas.coords(yilan[0]) #Yılanın başının koordinatları
    food_coords = canvas.coords(food)  #Yiyeceğin koordinatları

    yilan_dikdortgen = (yilan_coords[0], yilan_coords[1], yilan_coords[2], yilan_coords[3]) #Yılan başının koordinatlarına göre x1 y1 x2 ve y2 formatında döndürür.
    yiyecek_dikdortgen = (food_coords[0], food_coords[1], food_coords[2], food_coords[3])  #Alınan yiyecek koordinatlarını x1 y1 x2 ve y2 formatında döndürür.

    if yiyecek_dikdortgen_cakisiyormu(yilan_dikdortgen, yiyecek_dikdortgen):

        canvas.delete(food) #Yiyecek yenirse yiyeceği siler.
        food = yiyecek_olusturma() #Yiyecek yenince yeni yiyecek oluşturmak için fonksiyonu çağırır.
       
        son_parca = canvas.coords(yilan[-1]) #Yılanın son parçasının koordinatları -1 denilerek alınır ve yiyecek yenince yılanın yönüne göre yılan boyu uxatılır.
        if direction == 'up':
            yeni_parca = canvas.create_rectangle(son_parca[0], son_parca[1] + 10, son_parca[2], son_parca[3] + 10, fill='green', outline='green')
        elif direction == 'down':
            yeni_parca = canvas.create_rectangle(son_parca[0], son_parca[1] - 10, son_parca[2], son_parca[3] - 10, fill='green', outline='green')
        elif direction == 'right':
            yeni_parca = canvas.create_rectangle(son_parca[0] - 10, son_parca[1], son_parca[2] - 10, son_parca[3], fill='green', outline='green')
        elif direction == 'left':
            yeni_parca = canvas.create_rectangle(son_parca[0] + 10, son_parca[1], son_parca[2] + 10, son_parca[3], fill='green', outline='green')
        yilan.append(yeni_parca) #Oluşan yeni parça yılan listesine eklenir.

        score() #Yiyecek yenince skor değişsin.
        uygulama_bari() #Yiyecek yenince uygulama barı fonksiyonuna giderek gerekli değişimler yapılsın.
    

def yiyecek_dikdortgen_cakisiyormu(d1, d2): #İki dikdörtgenin x1,y1,x2 ve y2 noktlaraını temsil eder.
    return not (d1[2] <= d2[0] or d1[0] >= d2[2] or d1[3] <= d2[1] or d1[1] >= d2[3]) #Bu iki dikdörtgenin çakışmayacağı anlamına gelen noktlalar
   

def kendini_yeme():
    #Yılanın kendini yemesi sonucunda olacak değişimler burda gösterilir.
    global after_id
    yilan_basi = canvas.coords(yilan[0]) #Yılanın başının koordinatları alınır bu da yılanın şu anki pozisyonunu verir.

    for kalan_parcalar in yilan[1:]: #Yılanın ikinci parçasından itibaren olan parçaları alır.
        kalan_parcalarin_koordinatlari = canvas.coords(kalan_parcalar) # Bu parçaların koordiantları belirlenir.
        if yilan_basi == kalan_parcalarin_koordinatlari: #Eğer yılanın başının koordinatları kalan parçalarla aynı ise game over olur.
           game_over() 
           return


def reset_game():
    #Oyun tekrar başlayınca olan değişimler
    
    global root2 , food , canvas , direction , skor
    global  yenilen_yiyecek , bar , yenilen_yiyecekk 
    global yenilen_yiyecekkk , dolum_kismi , uygulama_bari1_label,ikon_bari,dikey_bar,dikey_bar2

    #Değişkenler sıfırlanndı.
    yenilen_yiyecek = 0
    yenilen_yiyecekk = 0
    yenilen_yiyecekkk = 0
    bar = 0

    direction = 'right' #Yılan her zaman sağ tarafa doğru hareket eder.
    
    #Skor sıfırlandı ve labele yansıtıldı.
    skor=0
    skor_label.config(text=f" {skor}")
    
    #Başlangıçta uygulama barı level1 ve mor olarak görünmesi için ayarlanması için uygulamabarı1 fonksiyonu  çağrıldı.
    uygulama_bari1_label.config(text="Level 1", bg='purple')
    uygulama_bari1()

    #Yiyecek yenmişse bar başlangıç haline getirildi.
    ilerleme_bari1.coords(dolum_kismi, (0, 0, 0, 15))
    ilerleme_bari1.itemconfig(dolum_kismi, fill='lightgrey')
    
    
    if 'root2' in globals(): #Bu şekilde tekrar oyna butonuna basınca game over ekranı kapatıldı.
           root2.destroy()

    
    canvas.delete(tk.ALL) #tk.all diyerek delete ile canvasın üstündeki tüm nesneler silinir.
    yilan.clear() #Yılan silinir.
    yilan.append(canvas.create_rectangle(15, 400, 30, 412, fill='green', outline='green'))#Yılan yeniden oluşturulur.

    #reset game ardından oyunun yeniden oynanabilmesi için fonksiyonlar çaprılır.
    food=yiyecek_olusturma()
    yon_belirleme() 
    uygulama_bari()
    bari_sifirlama()
    kendini_yeme()

    #Oyun tekrar başlayınca başlangıç ekranı açık yeşil yapılır.
    canvas.config(bg='lightgreen')
    #Hareket barları en baştaki hallerine döndürülür.
    dikey_bar = canvas2.create_rectangle(237, 203, 242, 280, fill='white',outline='lightgray')
    ikon_bari = canvas2.create_rectangle(50, 275, 220, 280, fill='white',outline='lightgray')
    dikey_bar2 = canvas2.create_rectangle(35, 302, 40, 430, fill='white',outline='lightgray')


def game_over():
        #Oyunda game over olduktan sonraki durumlar fonksiyonda uygulanır.
        global root2 , sad_face_foto

        root2 = tk.Toplevel(root) #Game over ekranı için bir root oluşturuldu ve rootun üstünde görünmesi için toplevel kullanıldı.
        root2.config(bg='purple') #Game over ekranının arka plan rengi mor yapıldı.
        root2.resizable(False, False)  #Game over ekranı sabit kalması için

        xx2 = (root2.winfo_screenwidth() / 2) -  (250 / 2) #root2.winfo_width ekranın toplam genişliğini alarak yarısını hesaplarız ve pencere genişliğinin yarısını da alarak pencereyi ortalarız.
        yy2 = (root2.winfo_screenheight() / 2) - (250 / 2)
        root2.geometry(f"{250}x{250}+{int(xx2)}+{int(yy2)}") #pencereyi 250x250 piksel ayarlar xx2 ve yy2 ise pencerenin konumunu verir.

        label = tk.Label(root2,text="GAME OVER",fg='yellow',bg='purple',font=("Helvetica",24),width=10,height=1)#Pencerede game over yazısı görünmesi için birlabel yani başlık oluşturuldu.
        label.pack(pady=5)#pady ile üst kenar ile arasında beş piksellik bir boşluk oluşturuldu.

        sad_face_yolu = 'C:/Users/guzel/Desktop/python/ikon/sad_face.png' #İkonun yolu
        sad_face_resmi = Image.open(sad_face_yolu) #ikon açıldı
        new_size = (75,75) #    İstenilen boyut
        sad_face_resmi = sad_face_resmi.resize(new_size) #İstenilen boyut resize ile uygulanarak yeni resim oluşturuldu
        sad_face_foto = ImageTk.PhotoImage(sad_face_resmi) #Yeni resim tkinterın kullanabileceği hale getirildi.
        sad_face_label = tk.Label(root2, image=sad_face_foto, bg='purple') #resmin nerde olacağı ,arka plan rengi belirlendi.
        sad_face_label.pack(pady=5) #resmin game over ekranındaki yeri


        #Reset game butonu için oluşturuldu. command ile reset game fonksiyonu bu iişlevi yerine getirdi.        
        button = tk.Button(root2,text="Tekrar Oyna",bg='black',fg='yellow',font=("Helvetica",14),command=reset_game)
        button.pack(pady=5)

        #Exit game butonu için oluşturuldu. command ile exit game fonksiyonu bu iişlevi yerine getirdi.       
        button_bitirme = tk.Button(root2, text = 'Çıkış', bg='yellow', fg='black',font=("Helvetica",14) , command=exit_game)
        button_bitirme.pack(pady=5)

        if after_id is not None:
          root.after_cancel(after_id)
          after_id = None #Zamanlayıcıyı sıfırlamak için kullanılır
        #finish()  



def exit_game(): #Game pver ekranında çıkış butonu için yazıldı.
    root.destroy() #root ekranını kapatmak için kullanılır.


def score():
    #Skorda güncelleme apabilmek için yazılan fonksiyon
    global skor

    #Skor her arttığında skoru güncelle ve ekranda göster.
    skor+=1
    skor_label.config(text=f"{skor}")
    en_yuksek()

    #if skor == 30: 
        #finish()


def en_yuksek():   
    global o_anki_skor , en_yuksek_skor

    o_anki_skor = skor
    #eğer oanki skor en yüksek skordan daha yüksekse en yüksek skoru güncelle.
    if skor > en_yuksek_skor:
        en_yuksek_skor=o_anki_skor
        en_yuksek_label.config(text=f"{en_yuksek_skor}")


def bari_sifirlama():
    #Barı sııfrlamak için kullanılır.
    global bar,yenilen_yiyecek , dolum_kismi , uygulama_bari1_label

    ilerleme_bari1.coords(dolum_kismi, (0, 0, 0, 15)) #İlerleme barını  başlangıç haline getirir.
    dolum_kismi = ilerleme_bari1.create_rectangle(0,0,0,15, fill='lightgray') #Dolum barını  başlangıç haline getirir.

    uygulama_bari1_label = tk.Label(root,text="Level 1",bg='purple',fg='white',width=5,height=1) #Level kısmını başlangıç seviyesine getirir.
    uygulama_bari1_label.place(x=580,y=125)
    uygulama_bari1()
    ilerleme_bari1.delete("all") #İlerleme barını sıfırlar.
    canvas2.coords
    canvas2.coords(dikey_bar, 237, 203, 242, 280)  # Dikey barın başlangıç koordinatları
    canvas2.coords(ikon_bari,50, 275, 220, 280)    # İkon barın başlangıç koordinatları
    canvas2.coords(dikey_bar2, 35, 302, 40, 430)  # Dikey bar2'nin başlangıç koordinatları
    yenilen_yiyecek=0
    

            
food = yiyecek_olusturma() 
yon_belirleme()
root.mainloop() #Rootun sürekli açık kalması sağlanır.