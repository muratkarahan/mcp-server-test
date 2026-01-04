import reedsolo
import os

# İlk 4 bayt
header = bytes.fromhex('1a cf fc 1d')

# Kodlanacak 1115 bayt
data = b'A' * 1115  # Örnek veri, kendi verinizle değiştirin

# RS(255, 223) için codec
rs = reedsolo.RSCodec(32)  # 32 parity, CCSDS RS(255,223)

coded_chunks = []

# 1115 baytı 223'lük parçalara bölüp her birini kodla
for i in range(0, 1115, 223):
    chunk = data[i:i+223]
    # Eksik ise padding (CCSDS genellikle sıfır ile doldurur)
    if len(chunk) < 223:
        chunk += b'\x00' * (223 - len(chunk))
    coded = rs.encode(chunk)  # 255 bayt olur
    coded_chunks.append(coded)

# Dosya yolunu ayarla
output_path = r"C:\Users\murat\workspace\mcp-server-test\test.bin"

# Dosyayı oluştur
with open(output_path, "wb") as f:
    f.write(header)
    for coded in coded_chunks:
        f.write(coded)
