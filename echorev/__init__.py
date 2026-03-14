#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EchoRev - A GUI tool for text direction reversal and RSA encryption/decryption.
"""

__version__ = '0.1.2'
__date__ = '2025-03-14'
__author__ = 'cycleuser'

version = __version__
date = __date__

import sys
import webbrowser
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QTextEdit, QMessageBox, QApplication,
    QFileDialog, QHBoxLayout, QVBoxLayout, QStatusBar, QMenuBar,
    QLabel, QGroupBox, QPushButton, QSizePolicy, QTabWidget
)
from PySide6.QtGui import QPixmap, QIcon, QAction, QPainter, QColor, QFont
from PySide6.QtCore import Qt, QTranslator, QLocale

import requests
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

LOCATION = Path(__file__).parent.resolve()


class Tr:
    """Translation helper."""
    _lang = 'en'
    
    LANGS = {
        'en': 'English',
        'zh': '中文',
        'ja': '日本語',
        'fr': 'Français',
        'ru': 'Русский',
        'de': 'Deutsch',
        'it': 'Italiano',
        'es': 'Español',
        'pt': 'Português',
        'ko': '한국어',
    }
    
    DATA = {
        'en': {
            'title': 'EchoRev',
            'tab_direction': 'Text Direction',
            'tab_crypto': 'Encryption / Decryption',
            'mode': 'Mode',
            'mode_horizontal': 'Horizontal Reverse',
            'mode_vertical': 'Vertical L→R',
            'mode_traditional': 'Traditional Chinese',
            'input': 'Input',
            'output': 'Output',
            'input_placeholder': 'Enter text here...',
            'output_placeholder': 'Result...',
            'keys': 'Keys',
            'gen_keys': 'Generate Keys',
            'load_priv': 'Load Private Key',
            'load_pub': 'Load Public Key',
            'keys_status': 'Keys: Not loaded',
            'priv_key': 'Private Key',
            'pub_key': 'Public Key',
            'plaintext': 'Plaintext',
            'ciphertext': 'Ciphertext (Hex)',
            'plain_placeholder': 'Enter plaintext...',
            'cipher_placeholder': 'Hex ciphertext...',
            'encrypt_btn': 'Encrypt →',
            'decrypt_btn': '← Decrypt',
            'menu_file': '&File',
            'menu_lang': '&Language',
            'menu_help': '&Help',
            'menu_quit': 'Quit',
            'menu_github': 'GitHub Repository',
            'menu_version': 'Check Version',
            'menu_about': 'About',
            'yes': 'Yes',
            'no': 'No',
            'confirm': 'Confirm',
            'keys_exist': 'Keys exist. Generate new ones?',
            'success': 'Success',
            'keys_ok': 'Keys generated!\n\nPrivate: {}\nPublic: {}',
            'error': 'Error',
            'keys_fail': 'Failed: {}',
            'warning': 'Warning',
            'need_pub': 'Please load a public key.',
            'no_plain': 'No plaintext to encrypt.',
            'no_cipher': 'No ciphertext to decrypt.',
            'pub_not_found': 'Public key file not found.',
            'priv_not_found': 'Private key file not found.',
            'enc_fail': 'Encryption failed: {}',
            'dec_fail': 'Decryption failed: {}',
            'bad_hex': 'Invalid hex string.',
            'need_priv': 'Please load a private key.',
            'save_priv': 'Save Private Key',
            'save_pub': 'Save Public Key',
            'open_priv': 'Open Private Key',
            'open_pub': 'Open Public Key',
            'pem_filter': 'PEM Files (*.pem);;All Files (*)',
            'version': 'Version',
            'ver_info': 'Current: v{}\nRemote: v{}\n\nReleased: {}',
            'net_err': 'Network Error',
            'ver_check_fail': 'Could not check updates.\n\nCurrent: v{}',
            'about_msg': 'EchoRev v{}\nReleased: {}\n\nText direction reversal & RSA encryption tool.\n\nhttps://github.com/cycleuser/EchoRev',
            'status': 'EchoRev v{} | {}',
        },
        'zh': {
            'title': 'EchoRev',
            'tab_direction': '文本方向',
            'tab_crypto': '加密 / 解密',
            'mode': '模式',
            'mode_horizontal': '水平反转',
            'mode_vertical': '垂直从左到右',
            'mode_traditional': '繁体中文',
            'input': '输入',
            'output': '输出',
            'input_placeholder': '在此输入文本...',
            'output_placeholder': '结果...',
            'keys': '密钥',
            'gen_keys': '生成密钥',
            'load_priv': '加载私钥',
            'load_pub': '加载公钥',
            'keys_status': '密钥：未加载',
            'priv_key': '私钥',
            'pub_key': '公钥',
            'plaintext': '明文',
            'ciphertext': '密文（十六进制）',
            'plain_placeholder': '输入明文...',
            'cipher_placeholder': '十六进制密文...',
            'encrypt_btn': '加密 →',
            'decrypt_btn': '← 解密',
            'menu_file': '文件(&F)',
            'menu_lang': '语言(&L)',
            'menu_help': '帮助(&H)',
            'menu_quit': '退出',
            'menu_github': 'GitHub 仓库',
            'menu_version': '检查版本',
            'menu_about': '关于',
            'yes': '是',
            'no': '否',
            'confirm': '确认',
            'keys_exist': '密钥已存在。是否生成新密钥？',
            'success': '成功',
            'keys_ok': '密钥已生成！\n\n私钥：{}\n公钥：{}',
            'error': '错误',
            'keys_fail': '失败：{}',
            'warning': '警告',
            'need_pub': '请先加载公钥。',
            'no_plain': '没有要加密的明文。',
            'no_cipher': '没有要解密的密文。',
            'pub_not_found': '公钥文件未找到。',
            'priv_not_found': '私钥文件未找到。',
            'enc_fail': '加密失败：{}',
            'dec_fail': '解密失败：{}',
            'bad_hex': '无效的十六进制字符串。',
            'need_priv': '请先加载私钥。',
            'save_priv': '保存私钥',
            'save_pub': '保存公钥',
            'open_priv': '打开私钥',
            'open_pub': '打开公钥',
            'pem_filter': 'PEM 文件 (*.pem);;所有文件 (*)',
            'version': '版本',
            'ver_info': '当前版本：v{}\n最新版本：v{}\n\n发布日期：{}',
            'net_err': '网络错误',
            'ver_check_fail': '无法检查更新。\n\n当前版本：v{}',
            'about_msg': 'EchoRev v{}\n发布日期：{}\n\n文本方向反转和RSA加密解密工具。\n\nhttps://github.com/cycleuser/EchoRev',
            'status': 'EchoRev v{} | {}',
        },
        'ja': {
            'title': 'EchoRev',
            'tab_direction': 'テキスト方向',
            'tab_crypto': '暗号化 / 復号化',
            'mode': 'モード',
            'mode_horizontal': '水平反転',
            'mode_vertical': '垂直 左→右',
            'mode_traditional': '繁体字中国語',
            'input': '入力',
            'output': '出力',
            'input_placeholder': 'テキストを入力...',
            'output_placeholder': '結果...',
            'keys': '鍵',
            'gen_keys': '鍵を生成',
            'load_priv': '秘密鍵を読み込む',
            'load_pub': '公開鍵を読み込む',
            'keys_status': '鍵：読み込まれていません',
            'priv_key': '秘密鍵',
            'pub_key': '公開鍵',
            'plaintext': '平文',
            'ciphertext': '暗号文（16進数）',
            'plain_placeholder': '平文を入力...',
            'cipher_placeholder': '16進数暗号文...',
            'encrypt_btn': '暗号化 →',
            'decrypt_btn': '← 復号化',
            'menu_file': 'ファイル(&F)',
            'menu_lang': '言語(&L)',
            'menu_help': 'ヘルプ(&H)',
            'menu_quit': '終了',
            'menu_github': 'GitHubリポジトリ',
            'menu_version': 'バージョン確認',
            'menu_about': 'について',
            'yes': 'はい',
            'no': 'いいえ',
            'confirm': '確認',
            'keys_exist': '鍵が存在します。新しく生成しますか？',
            'success': '成功',
            'keys_ok': '鍵が生成されました！\n\n秘密鍵：{}\n公開鍵：{}',
            'error': 'エラー',
            'keys_fail': '失敗：{}',
            'warning': '警告',
            'need_pub': '公開鍵を読み込んでください。',
            'no_plain': '暗号化する平文がありません。',
            'no_cipher': '復号化する暗号文がありません。',
            'pub_not_found': '公開鍵ファイルが見つかりません。',
            'priv_not_found': '秘密鍵ファイルが見つかりません。',
            'enc_fail': '暗号化失敗：{}',
            'dec_fail': '復号化失敗：{}',
            'bad_hex': '無効な16進数文字列です。',
            'need_priv': '秘密鍵を読み込んでください。',
            'save_priv': '秘密鍵を保存',
            'save_pub': '公開鍵を保存',
            'open_priv': '秘密鍵を開く',
            'open_pub': '公開鍵を開く',
            'pem_filter': 'PEMファイル (*.pem);;すべてのファイル (*)',
            'version': 'バージョン',
            'ver_info': '現在：v{}\n最新：v{}\n\nリリース：{}',
            'net_err': 'ネットワークエラー',
            'ver_check_fail': '更新を確認できません。\n\n現在：v{}',
            'about_msg': 'EchoRev v{}\nリリース：{}\n\nテキスト方向反転とRSA暗号化ツール。\n\nhttps://github.com/cycleuser/EchoRev',
            'status': 'EchoRev v{} | {}',
        },
        'fr': {
            'title': 'EchoRev',
            'tab_direction': 'Direction du texte',
            'tab_crypto': 'Chiffrement / Déchiffrement',
            'mode': 'Mode',
            'mode_horizontal': 'Inverser horizontalement',
            'mode_vertical': 'Vertical G→D',
            'mode_traditional': 'Chinois traditionnel',
            'input': 'Entrée',
            'output': 'Sortie',
            'input_placeholder': 'Entrez le texte...',
            'output_placeholder': 'Résultat...',
            'keys': 'Clés',
            'gen_keys': 'Générer les clés',
            'load_priv': 'Charger clé privée',
            'load_pub': 'Charger clé publique',
            'keys_status': 'Clés : Non chargées',
            'priv_key': 'Clé privée',
            'pub_key': 'Clé publique',
            'plaintext': 'Texte en clair',
            'ciphertext': 'Texte chiffré (Hex)',
            'plain_placeholder': 'Entrez le texte...',
            'cipher_placeholder': 'Hex chiffré...',
            'encrypt_btn': 'Chiffrer →',
            'decrypt_btn': '← Déchiffrer',
            'menu_file': '&Fichier',
            'menu_lang': '&Langue',
            'menu_help': '&Aide',
            'menu_quit': 'Quitter',
            'menu_github': 'Dépôt GitHub',
            'menu_version': 'Vérifier version',
            'menu_about': 'À propos',
            'yes': 'Oui',
            'no': 'Non',
            'confirm': 'Confirmer',
            'keys_exist': 'Les clés existent. En générer de nouvelles ?',
            'success': 'Succès',
            'keys_ok': 'Clés générées !\n\nPrivée : {}\nPublique : {}',
            'error': 'Erreur',
            'keys_fail': 'Échec : {}',
            'warning': 'Avertissement',
            'need_pub': 'Veuillez charger une clé publique.',
            'no_plain': 'Pas de texte à chiffrer.',
            'no_cipher': 'Pas de texte à déchiffrer.',
            'pub_not_found': 'Fichier clé publique introuvable.',
            'priv_not_found': 'Fichier clé privée introuvable.',
            'enc_fail': 'Échec chiffrement : {}',
            'dec_fail': 'Échec déchiffrement : {}',
            'bad_hex': 'Chaîne hex invalide.',
            'need_priv': 'Veuillez charger une clé privée.',
            'save_priv': 'Enregistrer clé privée',
            'save_pub': 'Enregistrer clé publique',
            'open_priv': 'Ouvrir clé privée',
            'open_pub': 'Ouvrir clé publique',
            'pem_filter': 'Fichiers PEM (*.pem);;Tous les fichiers (*)',
            'version': 'Version',
            'ver_info': 'Actuelle : v{}\nDernière : v{}\n\nPubliée : {}',
            'net_err': 'Erreur réseau',
            'ver_check_fail': 'Impossible de vérifier les mises à jour.\n\nActuelle : v{}',
            'about_msg': 'EchoRev v{}\nPubliée : {}\n\nOutil d\'inversion de texte et chiffrement RSA.\n\nhttps://github.com/cycleuser/EchoRev',
            'status': 'EchoRev v{} | {}',
        },
        'ru': {
            'title': 'EchoRev',
            'tab_direction': 'Направление текста',
            'tab_crypto': 'Шифрование / Расшифровка',
            'mode': 'Режим',
            'mode_horizontal': 'Горизонтальное отражение',
            'mode_vertical': 'Вертикально Л→П',
            'mode_traditional': 'Традиционный китайский',
            'input': 'Ввод',
            'output': 'Вывод',
            'input_placeholder': 'Введите текст...',
            'output_placeholder': 'Результат...',
            'keys': 'Ключи',
            'gen_keys': 'Создать ключи',
            'load_priv': 'Загрузить закр. ключ',
            'load_pub': 'Загрузить откр. ключ',
            'keys_status': 'Ключи: Не загружены',
            'priv_key': 'Закрытый ключ',
            'pub_key': 'Открытый ключ',
            'plaintext': 'Открытый текст',
            'ciphertext': 'Зашифрованный (Hex)',
            'plain_placeholder': 'Введите текст...',
            'cipher_placeholder': 'Hex текст...',
            'encrypt_btn': 'Зашифровать →',
            'decrypt_btn': '← Расшифровать',
            'menu_file': '&Файл',
            'menu_lang': '&Язык',
            'menu_help': '&Справка',
            'menu_quit': 'Выход',
            'menu_github': 'Репозиторий GitHub',
            'menu_version': 'Проверить версию',
            'menu_about': 'О программе',
            'yes': 'Да',
            'no': 'Нет',
            'confirm': 'Подтверждение',
            'keys_exist': 'Ключи существуют. Создать новые?',
            'success': 'Успех',
            'keys_ok': 'Ключи созданы!\n\nЗакрытый: {}\nОткрытый: {}',
            'error': 'Ошибка',
            'keys_fail': 'Ошибка: {}',
            'warning': 'Предупреждение',
            'need_pub': 'Загрузите открытый ключ.',
            'no_plain': 'Нет текста для шифрования.',
            'no_cipher': 'Нет текста для расшифровки.',
            'pub_not_found': 'Файл откр. ключа не найден.',
            'priv_not_found': 'Файл закр. ключа не найден.',
            'enc_fail': 'Ошибка шифрования: {}',
            'dec_fail': 'Ошибка расшифровки: {}',
            'bad_hex': 'Неверная hex-строка.',
            'need_priv': 'Загрузите закрытый ключ.',
            'save_priv': 'Сохранить закр. ключ',
            'save_pub': 'Сохранить откр. ключ',
            'open_priv': 'Открыть закр. ключ',
            'open_pub': 'Открыть откр. ключ',
            'pem_filter': 'PEM файлы (*.pem);;Все файлы (*)',
            'version': 'Версия',
            'ver_info': 'Текущая: v{}\nПоследняя: v{}\n\nОпубликовано: {}',
            'net_err': 'Ошибка сети',
            'ver_check_fail': 'Не удалось проверить обновления.\n\nТекущая: v{}',
            'about_msg': 'EchoRev v{}\nОпубликовано: {}\n\nИнструмент инверсии текста и RSA шифрования.\n\nhttps://github.com/cycleuser/EchoRev',
            'status': 'EchoRev v{} | {}',
        },
        'de': {
            'title': 'EchoRev',
            'tab_direction': 'Textrichtung',
            'tab_crypto': 'Verschlüsselung / Entschlüsselung',
            'mode': 'Modus',
            'mode_horizontal': 'Horizontal umkehren',
            'mode_vertical': 'Vertikal L→R',
            'mode_traditional': 'Traditionelles Chinesisch',
            'input': 'Eingabe',
            'output': 'Ausgabe',
            'input_placeholder': 'Text eingeben...',
            'output_placeholder': 'Ergebnis...',
            'keys': 'Schlüssel',
            'gen_keys': 'Schlüssel generieren',
            'load_priv': 'Priv. Schlüssel laden',
            'load_pub': 'Öff. Schlüssel laden',
            'keys_status': 'Schlüssel: Nicht geladen',
            'priv_key': 'Privater Schlüssel',
            'pub_key': 'Öffentlicher Schlüssel',
            'plaintext': 'Klartext',
            'ciphertext': 'Chiffretext (Hex)',
            'plain_placeholder': 'Klartext eingeben...',
            'cipher_placeholder': 'Hex-Chiffretext...',
            'encrypt_btn': 'Verschlüsseln →',
            'decrypt_btn': '← Entschlüsseln',
            'menu_file': '&Datei',
            'menu_lang': '&Sprache',
            'menu_help': '&Hilfe',
            'menu_quit': 'Beenden',
            'menu_github': 'GitHub Repository',
            'menu_version': 'Version prüfen',
            'menu_about': 'Über',
            'yes': 'Ja',
            'no': 'Nein',
            'confirm': 'Bestätigen',
            'keys_exist': 'Schlüssel existieren. Neue generieren?',
            'success': 'Erfolg',
            'keys_ok': 'Schlüssel generiert!\n\nPrivat: {}\nÖffentlich: {}',
            'error': 'Fehler',
            'keys_fail': 'Fehler: {}',
            'warning': 'Warnung',
            'need_pub': 'Bitte öffentlichen Schlüssel laden.',
            'no_plain': 'Kein Text zum Verschlüsseln.',
            'no_cipher': 'Kein Text zum Entschlüsseln.',
            'pub_not_found': 'Öff. Schlüsseldatei nicht gefunden.',
            'priv_not_found': 'Priv. Schlüsseldatei nicht gefunden.',
            'enc_fail': 'Verschlüsselung fehlgeschlagen: {}',
            'dec_fail': 'Entschlüsselung fehlgeschlagen: {}',
            'bad_hex': 'Ungültige Hex-Zeichenfolge.',
            'need_priv': 'Bitte privaten Schlüssel laden.',
            'save_priv': 'Priv. Schlüssel speichern',
            'save_pub': 'Öff. Schlüssel speichern',
            'open_priv': 'Priv. Schlüssel öffnen',
            'open_pub': 'Öff. Schlüssel öffnen',
            'pem_filter': 'PEM Dateien (*.pem);;Alle Dateien (*)',
            'version': 'Version',
            'ver_info': 'Aktuell: v{}\nNeueste: v{}\n\nVeröffentlicht: {}',
            'net_err': 'Netzwerkfehler',
            'ver_check_fail': 'Konnte Updates nicht prüfen.\n\nAktuell: v{}',
            'about_msg': 'EchoRev v{}\nVeröffentlicht: {}\n\nTextumkehrungs- und RSA-Verschlüsselungstool.\n\nhttps://github.com/cycleuser/EchoRev',
            'status': 'EchoRev v{} | {}',
        },
        'it': {
            'title': 'EchoRev',
            'tab_direction': 'Direzione testo',
            'tab_crypto': 'Crittografia / Decrittografia',
            'mode': 'Modalità',
            'mode_horizontal': 'Inversione orizzontale',
            'mode_vertical': 'Verticale S→D',
            'mode_traditional': 'Cinese tradizionale',
            'input': 'Input',
            'output': 'Output',
            'input_placeholder': 'Inserisci testo...',
            'output_placeholder': 'Risultato...',
            'keys': 'Chiavi',
            'gen_keys': 'Genera chiavi',
            'load_priv': 'Carica chiave privata',
            'load_pub': 'Carica chiave pubblica',
            'keys_status': 'Chiavi: Non caricate',
            'priv_key': 'Chiave privata',
            'pub_key': 'Chiave pubblica',
            'plaintext': 'Testo in chiaro',
            'ciphertext': 'Testo cifrato (Hex)',
            'plain_placeholder': 'Inserisci testo...',
            'cipher_placeholder': 'Hex cifrato...',
            'encrypt_btn': 'Cifra →',
            'decrypt_btn': '← Decifra',
            'menu_file': '&File',
            'menu_lang': '&Lingua',
            'menu_help': '&Aiuto',
            'menu_quit': 'Esci',
            'menu_github': 'Repository GitHub',
            'menu_version': 'Controlla versione',
            'menu_about': 'Informazioni',
            'yes': 'Sì',
            'no': 'No',
            'confirm': 'Conferma',
            'keys_exist': 'Le chiavi esistono. Generarne di nuove?',
            'success': 'Successo',
            'keys_ok': 'Chiavi generate!\n\nPrivata: {}\nPubblica: {}',
            'error': 'Errore',
            'keys_fail': 'Errore: {}',
            'warning': 'Avviso',
            'need_pub': 'Carica una chiave pubblica.',
            'no_plain': 'Nessun testo da cifrare.',
            'no_cipher': 'Nessun testo da decifrare.',
            'pub_not_found': 'File chiave pubblica non trovato.',
            'priv_not_found': 'File chiave privata non trovato.',
            'enc_fail': 'Crittografia fallita: {}',
            'dec_fail': 'Decrittografia fallita: {}',
            'bad_hex': 'Stringa hex non valida.',
            'need_priv': 'Carica una chiave privata.',
            'save_priv': 'Salva chiave privata',
            'save_pub': 'Salva chiave pubblica',
            'open_priv': 'Apri chiave privata',
            'open_pub': 'Apri chiave pubblica',
            'pem_filter': 'File PEM (*.pem);;Tutti i file (*)',
            'version': 'Versione',
            'ver_info': 'Attuale: v{}\nUltima: v{}\n\nPubblicata: {}',
            'net_err': 'Errore di rete',
            'ver_check_fail': 'Impossibile verificare aggiornamenti.\n\nAttuale: v{}',
            'about_msg': 'EchoRev v{}\nPubblicata: {}\n\nStrumento per inversione testo e crittografia RSA.\n\nhttps://github.com/cycleuser/EchoRev',
            'status': 'EchoRev v{} | {}',
        },
        'es': {
            'title': 'EchoRev',
            'tab_direction': 'Dirección del texto',
            'tab_crypto': 'Cifrado / Descifrado',
            'mode': 'Modo',
            'mode_horizontal': 'Invertir horizontal',
            'mode_vertical': 'Vertical I→D',
            'mode_traditional': 'Chino tradicional',
            'input': 'Entrada',
            'output': 'Salida',
            'input_placeholder': 'Ingrese texto...',
            'output_placeholder': 'Resultado...',
            'keys': 'Claves',
            'gen_keys': 'Generar claves',
            'load_priv': 'Cargar clave privada',
            'load_pub': 'Cargar clave pública',
            'keys_status': 'Claves: No cargadas',
            'priv_key': 'Clave privada',
            'pub_key': 'Clave pública',
            'plaintext': 'Texto plano',
            'ciphertext': 'Texto cifrado (Hex)',
            'plain_placeholder': 'Ingrese texto...',
            'cipher_placeholder': 'Hex cifrado...',
            'encrypt_btn': 'Cifrar →',
            'decrypt_btn': '← Descifrar',
            'menu_file': '&Archivo',
            'menu_lang': '&Idioma',
            'menu_help': '&Ayuda',
            'menu_quit': 'Salir',
            'menu_github': 'Repositorio GitHub',
            'menu_version': 'Verificar versión',
            'menu_about': 'Acerca de',
            'yes': 'Sí',
            'no': 'No',
            'confirm': 'Confirmar',
            'keys_exist': 'Las claves existen. ¿Generar nuevas?',
            'success': 'Éxito',
            'keys_ok': '¡Claves generadas!\n\nPrivada: {}\nPública: {}',
            'error': 'Error',
            'keys_fail': 'Error: {}',
            'warning': 'Advertencia',
            'need_pub': 'Cargue una clave pública.',
            'no_plain': 'No hay texto para cifrar.',
            'no_cipher': 'No hay texto para descifrar.',
            'pub_not_found': 'Archivo de clave pública no encontrado.',
            'priv_not_found': 'Archivo de clave privada no encontrado.',
            'enc_fail': 'Cifrado fallido: {}',
            'dec_fail': 'Descifrado fallido: {}',
            'bad_hex': 'Cadena hex inválida.',
            'need_priv': 'Cargue una clave privada.',
            'save_priv': 'Guardar clave privada',
            'save_pub': 'Guardar clave pública',
            'open_priv': 'Abrir clave privada',
            'open_pub': 'Abrir clave pública',
            'pem_filter': 'Archivos PEM (*.pem);;Todos los archivos (*)',
            'version': 'Versión',
            'ver_info': 'Actual: v{}\nÚltima: v{}\n\nPublicada: {}',
            'net_err': 'Error de red',
            'ver_check_fail': 'No se pudo verificar actualizaciones.\n\nActual: v{}',
            'about_msg': 'EchoRev v{}\nPublicada: {}\n\nHerramienta de inversión de texto y cifrado RSA.\n\nhttps://github.com/cycleuser/EchoRev',
            'status': 'EchoRev v{} | {}',
        },
        'pt': {
            'title': 'EchoRev',
            'tab_direction': 'Direção do texto',
            'tab_crypto': 'Criptografia / Descriptografia',
            'mode': 'Modo',
            'mode_horizontal': 'Inverter horizontal',
            'mode_vertical': 'Vertical E→D',
            'mode_traditional': 'Chinês tradicional',
            'input': 'Entrada',
            'output': 'Saída',
            'input_placeholder': 'Digite o texto...',
            'output_placeholder': 'Resultado...',
            'keys': 'Chaves',
            'gen_keys': 'Gerar chaves',
            'load_priv': 'Carregar chave privada',
            'load_pub': 'Carregar chave pública',
            'keys_status': 'Chaves: Não carregadas',
            'priv_key': 'Chave privada',
            'pub_key': 'Chave pública',
            'plaintext': 'Texto simples',
            'ciphertext': 'Texto cifrado (Hex)',
            'plain_placeholder': 'Digite o texto...',
            'cipher_placeholder': 'Hex cifrado...',
            'encrypt_btn': 'Cifrar →',
            'decrypt_btn': '← Decifrar',
            'menu_file': '&Arquivo',
            'menu_lang': '&Idioma',
            'menu_help': '&Ajuda',
            'menu_quit': 'Sair',
            'menu_github': 'Repositório GitHub',
            'menu_version': 'Verificar versão',
            'menu_about': 'Sobre',
            'yes': 'Sim',
            'no': 'Não',
            'confirm': 'Confirmar',
            'keys_exist': 'As chaves existem. Gerar novas?',
            'success': 'Sucesso',
            'keys_ok': 'Chaves geradas!\n\nPrivada: {}\nPública: {}',
            'error': 'Erro',
            'keys_fail': 'Erro: {}',
            'warning': 'Aviso',
            'need_pub': 'Carregue uma chave pública.',
            'no_plain': 'Sem texto para cifrar.',
            'no_cipher': 'Sem texto para decifrar.',
            'pub_not_found': 'Arquivo de chave pública não encontrado.',
            'priv_not_found': 'Arquivo de chave privada não encontrado.',
            'enc_fail': 'Criptografia falhou: {}',
            'dec_fail': 'Descriptografia falhou: {}',
            'bad_hex': 'String hex inválida.',
            'need_priv': 'Carregue uma chave privada.',
            'save_priv': 'Salvar chave privada',
            'save_pub': 'Salvar chave pública',
            'open_priv': 'Abrir chave privada',
            'open_pub': 'Abrir chave pública',
            'pem_filter': 'Arquivos PEM (*.pem);;Todos os arquivos (*)',
            'version': 'Versão',
            'ver_info': 'Atual: v{}\nÚltima: v{}\n\nPublicada: {}',
            'net_err': 'Erro de rede',
            'ver_check_fail': 'Não foi possível verificar atualizações.\n\nAtual: v{}',
            'about_msg': 'EchoRev v{}\nPublicada: {}\n\nFerramenta de inversão de texto e criptografia RSA.\n\nhttps://github.com/cycleuser/EchoRev',
            'status': 'EchoRev v{} | {}',
        },
        'ko': {
            'title': 'EchoRev',
            'tab_direction': '텍스트 방향',
            'tab_crypto': '암호화 / 복호화',
            'mode': '모드',
            'mode_horizontal': '수평 반전',
            'mode_vertical': '수직 L→R',
            'mode_traditional': '번체 중국어',
            'input': '입력',
            'output': '출력',
            'input_placeholder': '텍스트 입력...',
            'output_placeholder': '결과...',
            'keys': '키',
            'gen_keys': '키 생성',
            'load_priv': '개인 키 로드',
            'load_pub': '공개 키 로드',
            'keys_status': '키: 로드되지 않음',
            'priv_key': '개인 키',
            'pub_key': '공개 키',
            'plaintext': '평문',
            'ciphertext': '암호문 (Hex)',
            'plain_placeholder': '평문 입력...',
            'cipher_placeholder': 'Hex 암호문...',
            'encrypt_btn': '암호화 →',
            'decrypt_btn': '← 복호화',
            'menu_file': '파일(&F)',
            'menu_lang': '언어(&L)',
            'menu_help': '도움말(&H)',
            'menu_quit': '종료',
            'menu_github': 'GitHub 저장소',
            'menu_version': '버전 확인',
            'menu_about': '정보',
            'yes': '예',
            'no': '아니요',
            'confirm': '확인',
            'keys_exist': '키가 존재합니다. 새로 생성하시겠습니까?',
            'success': '성공',
            'keys_ok': '키가 생성되었습니다!\n\n개인 키: {}\n공개 키: {}',
            'error': '오류',
            'keys_fail': '오류: {}',
            'warning': '경고',
            'need_pub': '공개 키를 로드하세요.',
            'no_plain': '암호화할 평문이 없습니다.',
            'no_cipher': '복호화할 암호문이 없습니다.',
            'pub_not_found': '공개 키 파일을 찾을 수 없습니다.',
            'priv_not_found': '개인 키 파일을 찾을 수 없습니다.',
            'enc_fail': '암호화 실패: {}',
            'dec_fail': '복호화 실패: {}',
            'bad_hex': '잘못된 hex 문자열입니다.',
            'need_priv': '개인 키를 로드하세요.',
            'save_priv': '개인 키 저장',
            'save_pub': '공개 키 저장',
            'open_priv': '개인 키 열기',
            'open_pub': '공개 키 열기',
            'pem_filter': 'PEM 파일 (*.pem);;모든 파일 (*)',
            'version': '버전',
            'ver_info': '현재: v{}\n최신: v{}\n\n출시: {}',
            'net_err': '네트워크 오류',
            'ver_check_fail': '업데이트를 확인할 수 없습니다.\n\n현재: v{}',
            'about_msg': 'EchoRev v{}\n출시: {}\n\n텍스트 방향 반전 및 RSA 암호화 도구.\n\nhttps://github.com/cycleuser/EchoRev',
            'status': 'EchoRev v{} | {}',
        },
    }
    
    @classmethod
    def set_lang(cls, lang: str):
        cls._lang = lang
    
    @classmethod
    def get_lang(cls) -> str:
        return cls._lang
    
    @classmethod
    def t(cls, key: str) -> str:
        return cls.DATA.get(cls._lang, {}).get(key, cls.DATA['en'].get(key, key))
    
    @classmethod
    def detect_lang(cls) -> str:
        locale_map = {
            'zh': 'zh', 'ja': 'ja', 'fr': 'fr', 'ru': 'ru',
            'de': 'de', 'it': 'it', 'es': 'es', 'pt': 'pt', 'ko': 'ko',
        }
        sys_lang = QLocale.system().name()[:2]
        return locale_map.get(sys_lang, 'en')


class WatermarkTextEdit(QTextEdit):
    def __init__(self, placeholder_key: str, parent=None):
        super().__init__(parent)
        self._placeholder_key = placeholder_key
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def paintEvent(self, event):
        super().paintEvent(event)
        if self._placeholder_key and not self.toPlainText():
            painter = QPainter(self.viewport())
            painter.setPen(QColor(180, 180, 180, 150))
            painter.setFont(QFont("Arial", 16))
            painter.drawText(self.rect(), Qt.AlignCenter, Tr.t(self._placeholder_key))
            painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._priv_path = ''
        self._pub_path = ''
        self._mode = 0
        self._setup_ui()
        
        lang = Tr.detect_lang()
        Tr.set_lang(lang)
        self._update_ui()
    
    def _setup_ui(self):
        self.setMinimumSize(800, 600)
        self.resize(900, 650)
        
        icon_path = LOCATION / 'icon.png'
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        self._tabs = QTabWidget()
        layout.addWidget(self._tabs)
        
        dir_widget = QWidget()
        dir_layout = QVBoxLayout(dir_widget)
        dir_layout.setContentsMargins(5, 5, 5, 5)
        
        dir_text_layout = QHBoxLayout()
        
        self._input_group = QGroupBox()
        input_layout = QVBoxLayout(self._input_group)
        self._input = WatermarkTextEdit('input_placeholder')
        self._input.textChanged.connect(self._on_input_changed)
        input_layout.addWidget(self._input)
        dir_text_layout.addWidget(self._input_group)
        
        self._output_group = QGroupBox()
        output_layout = QVBoxLayout(self._output_group)
        self._output = WatermarkTextEdit('output_placeholder')
        self._output.setReadOnly(True)
        output_layout.addWidget(self._output)
        dir_text_layout.addWidget(self._output_group)
        
        dir_layout.addLayout(dir_text_layout, 1)
        self._tabs.addTab(dir_widget, "")
        
        crypto_widget = QWidget()
        crypto_layout = QVBoxLayout(crypto_widget)
        crypto_layout.setContentsMargins(5, 5, 5, 5)
        
        status_layout = QHBoxLayout()
        self._status_label = QLabel()
        status_layout.addWidget(self._status_label)
        status_layout.addStretch()
        crypto_layout.addLayout(status_layout)
        
        crypto_text_layout = QHBoxLayout()
        
        self._plain_group = QGroupBox()
        plain_layout = QVBoxLayout(self._plain_group)
        self._plain = WatermarkTextEdit('plain_placeholder')
        plain_layout.addWidget(self._plain)
        
        self._btn_encrypt = QPushButton()
        self._btn_encrypt.clicked.connect(self._encrypt)
        plain_layout.addWidget(self._btn_encrypt)
        crypto_text_layout.addWidget(self._plain_group)
        
        self._cipher_group = QGroupBox()
        cipher_layout = QVBoxLayout(self._cipher_group)
        self._cipher = WatermarkTextEdit('cipher_placeholder')
        cipher_layout.addWidget(self._cipher)
        
        self._btn_decrypt = QPushButton()
        self._btn_decrypt.clicked.connect(self._decrypt)
        cipher_layout.addWidget(self._btn_decrypt)
        crypto_text_layout.addWidget(self._cipher_group)
        
        crypto_layout.addLayout(crypto_text_layout, 1)
        self._tabs.addTab(crypto_widget, "")
        
        self._create_menu()
        
        self._statusbar = QStatusBar()
        self.setStatusBar(self._statusbar)
    
    def _create_menu(self):
        menubar = self.menuBar()
        
        self._file_menu = menubar.addMenu("")
        
        self._act_gen_keys = QAction("", self)
        self._act_gen_keys.triggered.connect(self._gen_keys)
        self._file_menu.addAction(self._act_gen_keys)
        
        self._act_load_priv = QAction("", self)
        self._act_load_priv.triggered.connect(self._load_priv)
        self._file_menu.addAction(self._act_load_priv)
        
        self._act_load_pub = QAction("", self)
        self._act_load_pub.triggered.connect(self._load_pub)
        self._file_menu.addAction(self._act_load_pub)
        
        self._file_menu.addSeparator()
        
        self._act_quit = QAction("", self)
        self._act_quit.setShortcut('Ctrl+Q')
        self._act_quit.triggered.connect(QApplication.quit)
        self._file_menu.addAction(self._act_quit)
        
        self._mode_menu = menubar.addMenu("")
        self._mode_actions = []
        for i, key in enumerate(['mode_horizontal', 'mode_vertical', 'mode_traditional']):
            act = QAction("", self)
            act.setCheckable(True)
            act.triggered.connect(lambda checked, m=i: self._set_mode(m))
            self._mode_menu.addAction(act)
            self._mode_actions.append(act)
        self._mode_actions[0].setChecked(True)
        
        self._lang_menu = menubar.addMenu("")
        for code, name in Tr.LANGS.items():
            act = QAction(name, self)
            act.triggered.connect(lambda checked, c=code: self._change_lang(c))
            self._lang_menu.addAction(act)
        
        self._help_menu = menubar.addMenu("")
        
        self._act_github = QAction("", self)
        self._act_github.triggered.connect(lambda: webbrowser.open('https://github.com/cycleuser/EchoRev'))
        self._help_menu.addAction(self._act_github)
        
        self._act_version = QAction("", self)
        self._act_version.triggered.connect(self._check_version)
        self._help_menu.addAction(self._act_version)
        
        self._help_menu.addSeparator()
        
        self._act_about = QAction("", self)
        self._act_about.triggered.connect(self._show_about)
        self._help_menu.addAction(self._act_about)
    
    def _set_mode(self, mode: int):
        self._mode = mode
        for i, act in enumerate(self._mode_actions):
            act.setChecked(i == mode)
        self._on_input_changed()
    
    def _change_lang(self, lang: str):
        Tr.set_lang(lang)
        self._update_ui()
    
    def _update_ui(self):
        self.setWindowTitle(f"{Tr.t('title')} v{version}")
        self._tabs.setTabText(0, Tr.t('tab_direction'))
        self._tabs.setTabText(1, Tr.t('tab_crypto'))
        
        self._file_menu.setTitle(Tr.t('menu_file'))
        self._act_gen_keys.setText(Tr.t('gen_keys'))
        self._act_load_priv.setText(Tr.t('load_priv'))
        self._act_load_pub.setText(Tr.t('load_pub'))
        self._act_quit.setText(Tr.t('menu_quit'))
        
        self._mode_menu.setTitle(Tr.t('mode'))
        for i, key in enumerate(['mode_horizontal', 'mode_vertical', 'mode_traditional']):
            self._mode_actions[i].setText(Tr.t(key))
        
        self._lang_menu.setTitle(Tr.t('menu_lang'))
        
        self._help_menu.setTitle(Tr.t('menu_help'))
        self._act_github.setText(Tr.t('menu_github'))
        self._act_version.setText(Tr.t('menu_version'))
        self._act_about.setText(Tr.t('menu_about'))
        
        self._input_group.setTitle(Tr.t('input'))
        self._output_group.setTitle(Tr.t('output'))
        self._plain_group.setTitle(Tr.t('plaintext'))
        self._cipher_group.setTitle(Tr.t('ciphertext'))
        self._btn_encrypt.setText(Tr.t('encrypt_btn'))
        self._btn_decrypt.setText(Tr.t('decrypt_btn'))
        
        self._update_key_status()
        self._statusbar.showMessage(Tr.t('status').format(version, date))
    
    def _update_key_status(self):
        if self._priv_path or self._pub_path:
            priv_name = Path(self._priv_path).name if self._priv_path else '-'
            pub_name = Path(self._pub_path).name if self._pub_path else '-'
            self._status_label.setText(f"{Tr.t('priv_key')}: {priv_name} | {Tr.t('pub_key')}: {pub_name}")
        else:
            self._status_label.setText(Tr.t('keys_status'))
    
    def _on_input_changed(self):
        text = self._input.toPlainText()
        if not text:
            self._output.clear()
            return
        
        lines = text.split('\n')
        
        if self._mode == 0:
            result = '\n'.join(line[::-1] for line in lines)
        else:
            max_len = max((len(line) for line in lines), default=0)
            result_lines = []
            for i in range(max_len):
                chars = []
                for line in lines:
                    if i < len(line):
                        chars.append(line[i])
                    else:
                        fill = '\u3000' if any('\u4e00' <= c <= '\u9fff' for c in text) else ' '
                        chars.append(fill)
                col = ''.join(chars)
                if self._mode == 2:
                    col = col[::-1]
                result_lines.append(col)
            result = '\n'.join(result_lines)
        
        self._output.setPlainText(result)
    
    def _gen_keys(self):
        if self._priv_path or self._pub_path:
            if QMessageBox.question(self, Tr.t('confirm'), Tr.t('keys_exist'),
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return
        
        filt = Tr.t('pem_filter')
        priv, _ = QFileDialog.getSaveFileName(self, Tr.t('save_priv'), "private_key.pem", filt)
        if not priv:
            return
        
        pub, _ = QFileDialog.getSaveFileName(self, Tr.t('save_pub'), "public_key.pem", filt)
        if not pub:
            return
        
        try:
            priv_key = rsa.generate_private_key(65537, 2048, default_backend())
            pub_key = priv_key.public_key()
            
            with open(priv, 'wb') as f:
                f.write(priv_key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.TraditionalOpenSSL,
                    serialization.NoEncryption()
                ))
            
            with open(pub, 'wb') as f:
                f.write(pub_key.public_bytes(
                    serialization.Encoding.PEM,
                    serialization.PublicFormat.SubjectPublicKeyInfo
                ))
            
            self._priv_path = priv
            self._pub_path = pub
            self._update_key_status()
            
            QMessageBox.information(self, Tr.t('success'), Tr.t('keys_ok').format(priv, pub))
        except Exception as e:
            QMessageBox.critical(self, Tr.t('error'), Tr.t('keys_fail').format(e))
    
    def _load_priv(self):
        path, _ = QFileDialog.getOpenFileName(self, Tr.t('open_priv'), "", Tr.t('pem_filter'))
        if path:
            self._priv_path = path
            self._update_key_status()
    
    def _load_pub(self):
        path, _ = QFileDialog.getOpenFileName(self, Tr.t('open_pub'), "", Tr.t('pem_filter'))
        if path:
            self._pub_path = path
            self._update_key_status()
    
    def _encrypt(self):
        if not self._pub_path:
            QMessageBox.warning(self, Tr.t('warning'), Tr.t('need_pub'))
            return
        
        plain = self._plain.toPlainText()
        if not plain:
            QMessageBox.warning(self, Tr.t('warning'), Tr.t('no_plain'))
            return
        
        try:
            with open(self._pub_path, 'rb') as f:
                pub_key = serialization.load_pem_public_key(f.read(), backend=default_backend())
            
            chunks = []
            for i in range(0, len(plain), 190):
                chunk = plain[i:i+190].encode('utf-8')
                enc = pub_key.encrypt(chunk, padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(), label=None
                ))
                chunks.append(enc)
            
            self._cipher.setPlainText(b''.join(chunks).hex())
        except FileNotFoundError:
            QMessageBox.critical(self, Tr.t('error'), Tr.t('pub_not_found'))
        except Exception as e:
            QMessageBox.critical(self, Tr.t('error'), Tr.t('enc_fail').format(e))
    
    def _decrypt(self):
        if not self._priv_path:
            QMessageBox.warning(self, Tr.t('warning'), Tr.t('need_priv'))
            return
        
        hex_text = self._cipher.toPlainText()
        if not hex_text:
            QMessageBox.warning(self, Tr.t('warning'), Tr.t('no_cipher'))
            return
        
        try:
            data = bytes.fromhex(hex_text.strip())
        except ValueError:
            QMessageBox.critical(self, Tr.t('error'), Tr.t('bad_hex'))
            return
        
        try:
            with open(self._priv_path, 'rb') as f:
                priv_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
            
            chunks = []
            for i in range(0, len(data), 256):
                chunk = data[i:i+256]
                dec = priv_key.decrypt(chunk, padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(), label=None
                ))
                chunks.append(dec)
            
            self._plain.setPlainText(b''.join(chunks).decode('utf-8'))
        except FileNotFoundError:
            QMessageBox.critical(self, Tr.t('error'), Tr.t('priv_not_found'))
        except Exception as e:
            QMessageBox.critical(self, Tr.t('error'), Tr.t('dec_fail').format(e))
    
    def _check_version(self):
        try:
            r = requests.get(
                'https://raw.githubusercontent.com/cycleuser/EchoRev/master/echorev/__init__.py',
                timeout=10
            )
            r.raise_for_status()
            for line in r.text.splitlines():
                if line.startswith('__version__'):
                    remote = line.split('=')[1].strip().strip("'\"")
                    break
            else:
                remote = 'unknown'
            QMessageBox.information(self, Tr.t('version'), Tr.t('ver_info').format(version, remote, date))
        except Exception:
            QMessageBox.warning(self, Tr.t('net_err'), Tr.t('ver_check_fail').format(version))
    
    def _show_about(self):
        QMessageBox.about(self, Tr.t('menu_about'), Tr.t('about_msg').format(version, date))


def main():
    app = QApplication(sys.argv)
    app.installTranslator(QTranslator())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()