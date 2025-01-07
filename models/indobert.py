
import pickle
import re
from nltk.corpus import stopwords

class SentimentAnalyzer:
    def __init__(self, model_path, vectorizer_path):
        # Load model SVM dan vectorizer
        with open(model_path, 'rb') as model_file:
            self.model = pickle.load(model_file)
        with open(vectorizer_path, 'rb') as vectorizer_file:
            self.vectorizer = pickle.load(vectorizer_file)

        # Stop words dan normalisasi teks
        self.stop_words = set(stopwords.words('indonesian'))
        self.words_dict = {
                   'tdk': 'tidak', 'yg': 'yang', 'ga': 'tidak', 'gak': 'tidak', 'tp': 'tapi', 'd': 'di',
            'sy': 'saya', '&': 'dan', 'dgn': 'dengan', 'utk': 'untuk', 'gk': 'tidak', 'jd': 'jadi',
            'jg': 'juga', 'dr': 'dari', 'krn': 'karena', 'aja': 'saja', 'karna': 'karena', 'udah': 'sudah',
            'kmr': 'kamar', 'g': 'tidak', 'dpt': 'dapat', 'banget': 'sekali', 'bgt': 'sekali', 'kalo': 'kalau',
            'n': 'dan', 'bs': 'bisa', 'oke': 'ok', 'dg': 'dengan', 'pake': 'pakai', 'sampe': 'sampai',
            'dapet': 'dapat', 'ad': 'ada', 'lg': 'lagi', 'bikin': 'buat', 'tak': 'tidak', 'ny': 'nya',
            'ngga': 'tidak', 'nunggu': 'tunggu', 'klo': 'kalau', 'blm': 'belum', 'trus': 'terus', 'kayak': 'seperti',
            'dlm': 'dalam', 'udh': 'sudah', 'tau': 'tahu', 'org': 'orang', 'hrs': 'harus', 'msh': 'masih',
            'sm': 'sama', 'byk': 'banyak', 'krg': 'kurang', 'kmar': 'kamar', 'spt': 'seperti', 'pdhl': 'padahal',
            'chek': 'cek', 'pesen': 'pesan', 'kran': 'keran', 'gitu': 'begitu', 'tpi': 'tapi', 'lbh': 'lebih',
            'tmpt': 'tempat', 'dikasi': 'dikasih', 'serem': 'seram', 'sya': 'saya', 'jgn': 'jangan',
            'dri': 'dari', 'dtg': 'datang', 'gada': 'tidak ada', 'standart': 'standar', 'mlm': 'malam',
            'k': 'ke', 'kl': 'kalau', 'sgt': 'sangat', 'y': 'ya', 'krna': 'karena', 'tgl': 'tanggal',
            'terimakasih': 'terima kasih', 'kecoak': 'kecoa', 'pd': 'pada', 'tdr': 'tidur', 'jdi': 'jadi',
            'kyk': 'seperti', 'sdh': 'sudah', 'ama': 'sama', 'gmana': 'bagaimana', 'dalem': 'dalam',
            'tanyak': 'tanya', 'taru': 'taruh', 'gede': 'besar', 'kaya': 'seperti', 'access': 'akses',
            'tetep': 'tetap', 'mgkin': 'mungkin', 'sower': 'shower', 'idup': 'hidup', 'nyaaa': 'nya',
            'baikk': 'baik', 'hanay': 'hanya', 'tlp': 'telpon', 'kluarga': 'keluarga', 'jln': 'jalan',
            'hr': 'hari', 'ngak': 'tidak', 'bli': 'beli', 'kmar': 'kamar', 'naro': 'taruh'
        }
        self.stop_words = set(stopwords.words('indonesian'))

    def clean_text(self, text):
        # Preprocessing teks
        text = text.lower()
        for word, replacement in self.words_dict.items():
            text = re.sub(r'\b' + re.escape(word) + r'\b', replacement, text)
        text = ' '.join([word for word in text.split() if word not in self.stop_words])
        return text

    def predict_sentiment(self, text):
        # Preprocess teks
        clean_text = self.clean_text(text)
        # Transform teks menggunakan vectorizer
        features = self.vectorizer.transform([clean_text])
        # Prediksi sentimen
        prediction = self.model.predict(features)
        return prediction[0]  # 0 untuk Negatif, 1 untuk Positif
