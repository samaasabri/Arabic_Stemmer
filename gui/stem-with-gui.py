import typing
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QWidget
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
arabic_stop_words = set(stopwords.words('arabic'))


def remove_non_arabic_chars(text):
    # Remove non-Arabic characters from the text
    output_string = re.sub(r'[^\u0600-\u06FF\u0750-\u077F]+', ' ', text)
    return output_string


def tokenize(text):
    # Tokenize the Arabic text
    return re.findall(r'\b\w+\b', text)


def remove_diacritics(text):
    # Remove diacritics (vowel marks) from the Arabic text
    diacritic_marks = ['َ', 'ُ', 'ِ', 'ْ', 'ّ', 'ٌ', 'ً', 'ٍ']
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    for mark in diacritic_marks:
        text = text.replace(mark, '')
    return text


def normalize(word):
    # Remove common Arabic prefixes and suffixes
    prefixes = ['ال', 'و', 'ف', 'ب', 'ك', 'ل', 'ت']
    suffixes = ['ة', 'ي', 'ه', 'نا', 'كم', 'هما', 'كن', 'ن', 'ا', 'ت']
    prefixes.reverse()
    suffixes.reverse()
    for prefix in prefixes:
        if word.startswith(prefix):
            word = word[len(prefix):]
            break

    for suffix in suffixes:
        if word.endswith(suffix):
            word = word[:-len(suffix)]
            break
    word = word.replace('ى', 'ي')
    return word


def apply_prefix_rules(word):
    # Apply the ISRI stemmer prefix rules to the word
    # This involves removing additional prefixes based on the context of the word
    # You can find the complete set of prefix rules in the ISRI stemmer paper
    if word.startswith('و'):
        if word[1:].startswith(('ل', 'س', 'ي', 'ن')):
            word = word[1:]
    if word.startswith(('الم', 'ال')):
        word = word[3:]
    if word.startswith('لل'):
        word = word[2:]
    return word


def apply_suffix_rules(word):
    # Apply the ISRI stemmer suffix rules to the word
    # This involves removing additional suffixes based on the context of the word
    # You can find the complete set of suffix rules in the ISRI stemmer paper
    if word.endswith(('ات', 'ون', 'ين', 'تن', 'يه', 'ة', 'و')):
        word = word[:-1]
    if word.endswith('ان'):
        if len(word) > 4:
            word = word[:-2]
        else:
            word = word[:-1]
    if word.endswith(('تما', 'تان', 'كما', 'هما', 'نا')):
        word = word[:-2]
    if word.endswith(('وا', 'يا', 'ا')):
        word = word[:-1]
    return word


def stem(text):
    tokens = remove_non_arabic_chars(text)
    # Tokenize the text into individual words
    tokens = tokenize(tokens)

    # Stem each token
    stemmed_tokens = []
    for token in tokens:
        if (len(token) > 3):
            if (token[-1] == 'ى'):
                token = remove_diacritics(token)
                # token = remove_non_arabic_chars(token)
                token = normalize(token)
                token = apply_prefix_rules(token)
            else:
                token = remove_diacritics(token)
                # token = remove_non_arabic_chars(token)
                token = normalize(token)
                token = apply_prefix_rules(token)
                token = apply_suffix_rules(token)

            # Add the stemmed token to the list
        stemmed_tokens.append(token)

    # Return the stemmed text
    return ' '.join(stemmed_tokens)


arabic_stop_words.remove('علم')
arabic_stop_words.remove('أبريل')
arabic_stop_words.remove('أيلول')
arabic_stop_words.remove('سبتمبر')
arabic_stop_words.remove('ريال')
arabic_stop_words.remove('أكتوبر')
arabic_stop_words.remove('أغسطس')
arabic_stop_words.remove('شمال')
arabic_stop_words.remove('دولار')
arabic_stop_words.remove('أمامكَ')
arabic_stop_words.remove('يوليو')
arabic_stop_words.remove('حبيب')
arabic_stop_words.remove('فبراير')
arabic_stop_words.remove('درهم')
arabic_stop_words.remove('يونيو')

text = '''اكان علم النفس دائما بالجامعات بتقاليده الدنيوية )غير
الدينية( الملتزمة بالتنوير. وكان - على الدوام- من ضمن هذه
التقاليد وجود شك واضح بكل أشكال التدين، كما يصف بيرنارد
.غروم
'''
text2 = "الكلبان يلعبان في الحديقة eng"
text3 = "الكلبان يلعبان &*^%َ في الحديقة "


filtered_words = []
original_words = []


class stem_ui(QMainWindow):

    def __init__(self):
        super(stem_ui, self).__init__()
        uic.loadUi("gui/stemmer.ui", self)
        self.table1.setColumnWidth(0, 160)
        self.table1.setColumnWidth(1, 160)
        self.show()
        self.btn1.clicked.connect(self.on_clicked)

    def on_clicked(self):

        input_from_gui = self.textBox.toPlainText()

        words = input_from_gui.split()

        filtered_words = [stem(word)
                          for word in words if not word in arabic_stop_words]

        for word in filtered_words:
            if word == '':
                filtered_words.remove(word)

        output_text = ' '.join(filtered_words)

        original_words = [word for word in words if stem(
            word) in filtered_words and word != '']

        self.table1.setRowCount(len(filtered_words))

        row = 0
        for orig_word in original_words:
            self.table1.setItem(row, 0, QTableWidgetItem(orig_word))
            row = row + 1

        row = 0
        for stemmed_word in filtered_words:
            self.table1.setItem(row, 1, QTableWidgetItem(stemmed_word))
            row = row + 1


def main():
    app = QApplication([])
    window = stem_ui()
    app.exec_()


if __name__ == '__main__':
    main()
