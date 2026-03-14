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
from typing import Dict, Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QTextEdit, QMessageBox, QApplication,
    QFileDialog, QHBoxLayout, QVBoxLayout, QStatusBar, QMenuBar,
    QLabel, QSlider, QGroupBox, QPushButton, QSizePolicy, QTabWidget,
    QMenu
)
from PySide6.QtGui import QPixmap, QIcon, QAction, QPainter, QColor, QFont
from PySide6.QtCore import Qt, QTranslator, QLocale

import requests
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

LOCATION = Path(__file__).parent.resolve()


class I18N:
    """Internationalization manager."""
    
    LANGUAGES = {
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
    
    TRANSLATIONS: Dict[str, Dict[str, str]] = {
        'en': {
            'app_title': 'EchoRev',
            'tab_text_direction': 'Text Direction',
            'tab_encryption': 'Encryption / Decryption',
            'direction_mode': 'Direction Mode',
            'horizontal_reverse': 'Horizontal Reverse',
            'vertical_lr': 'Vertical L→R',
            'traditional_chinese': 'Traditional Chinese',
            'text_input': 'Text Input',
            'text_output': 'Text Output',
            'enter_text': 'Enter text here...',
            'converted_text': 'Converted text...',
            'key_management': 'Key Management',
            'generate_keys': 'Generate Keys',
            'load_private_key': 'Load Private Key',
            'load_public_key': 'Load Public Key',
            'keys_not_loaded': 'Keys: Not loaded',
            'private_key': 'Private Key',
            'public_key': 'Public Key',
            'plaintext': 'Plaintext',
            'ciphertext': 'Ciphertext (Hex)',
            'enter_plaintext': 'Enter plaintext here...',
            'encrypted_hex': 'Encrypted hex text...',
            'encrypt': 'Encrypt →',
            'decrypt': '← Decrypt',
            'file': '&File',
            'quit': 'Quit',
            'language': '&Language',
            'help': '&Help',
            'github': 'GitHub Repository',
            'check_version': 'Check Version',
            'about': 'About',
            'confirm': 'Confirm',
            'keys_exist': 'Keys already exist. Generate new keys?',
            'yes': 'Yes',
            'no': 'No',
            'success': 'Success',
            'keys_generated': 'Keys generated!\n\nPrivate: {}\nPublic: {}',
            'error': 'Error',
            'failed_generate_keys': 'Failed to generate keys:\n{}',
            'warning': 'Warning',
            'load_public_first': 'Please load a public key first.',
            'no_plaintext': 'No plaintext to encrypt.',
            'no_ciphertext': 'No ciphertext to decrypt.',
            'public_key_not_found': 'Public key file not found.',
            'private_key_not_found': 'Private key file not found.',
            'encryption_failed': 'Encryption failed:\n{}',
            'decryption_failed': 'Decryption failed:\n{}',
            'invalid_hex': 'Invalid hex string.',
            'load_private_first': 'Please load a private key first.',
            'save_private_key': 'Save Private Key',
            'save_public_key': 'Save Public Key',
            'open_private_key': 'Open Private Key',
            'open_public_key': 'Open Public Key',
            'pem_files': 'PEM Files (*.pem);;All Files (*)',
            'version': 'Version',
            'current_remote': 'Current: v{}\nRemote: v{}\n\nReleased: {}',
            'network_error': 'Network Error',
            'could_not_check': 'Could not check for updates.\n\nCurrent version: v{}',
            'about_text': 'EchoRev v{}\nReleased: {}\n\nA GUI tool for text direction reversal\nand RSA encryption/decryption.\n\nhttps://github.com/cycleuser/EchoRev',
            'status_bar': 'EchoRev v{} | Released: {}',
        },
        'zh': {
            'app_title': 'EchoRev',
            'tab_text_direction': '文本方向',
            'tab_encryption': '加密 / 解密',
            'direction_mode': '方向模式',
            'horizontal_reverse': '水平反转',
            'vertical_lr': '垂直从左到右',
            'traditional_chinese': '繁体中文',
            'text_input': '文本输入',
            'text_output': '文本输出',
            'enter_text': '在此输入文本...',
            'converted_text': '转换后的文本...',
            'key_management': '密钥管理',
            'generate_keys': '生成密钥',
            'load_private_key': '加载私钥',
            'load_public_key': '加载公钥',
            'keys_not_loaded': '密钥：未加载',
            'private_key': '私钥',
            'public_key': '公钥',
            'plaintext': '明文',
            'ciphertext': '密文（十六进制）',
            'enter_plaintext': '在此输入明文...',
            'encrypted_hex': '加密后的十六进制文本...',
            'encrypt': '加密 →',
            'decrypt': '← 解密',
            'file': '文件(&F)',
            'quit': '退出',
            'language': '语言(&L)',
            'help': '帮助(&H)',
            'github': 'GitHub 仓库',
            'check_version': '检查版本',
            'about': '关于',
            'confirm': '确认',
            'keys_exist': '密钥已存在。是否生成新密钥？',
            'yes': '是',
            'no': '否',
            'success': '成功',
            'keys_generated': '密钥已生成！\n\n私钥：{}\n公钥：{}',
            'error': '错误',
            'failed_generate_keys': '生成密钥失败：\n{}',
            'warning': '警告',
            'load_public_first': '请先加载公钥。',
            'no_plaintext': '没有要加密的明文。',
            'no_ciphertext': '没有要解密的密文。',
            'public_key_not_found': '公钥文件未找到。',
            'private_key_not_found': '私钥文件未找到。',
            'encryption_failed': '加密失败：\n{}',
            'decryption_failed': '解密失败：\n{}',
            'invalid_hex': '无效的十六进制字符串。',
            'load_private_first': '请先加载私钥。',
            'save_private_key': '保存私钥',
            'save_public_key': '保存公钥',
            'open_private_key': '打开私钥',
            'open_public_key': '打开公钥',
            'pem_files': 'PEM 文件 (*.pem);;所有文件 (*)',
            'version': '版本',
            'current_remote': '当前版本：v{}\n最新版本：v{}\n\n发布日期：{}',
            'network_error': '网络错误',
            'could_not_check': '无法检查更新。\n\n当前版本：v{}',
            'about_text': 'EchoRev v{}\n发布日期：{}\n\n文本方向反转和RSA加密解密工具。\n\nhttps://github.com/cycleuser/EchoRev',
            'status_bar': 'EchoRev v{} | 发布日期：{}',
        },
        'ja': {
            'app_title': 'EchoRev',
            'tab_text_direction': 'テキスト方向',
            'tab_encryption': '暗号化 / 復号化',
            'direction_mode': '方向モード',
            'horizontal_reverse': '水平反転',
            'vertical_lr': '垂直 左→右',
            'traditional_chinese': '繁体字中国語',
            'text_input': 'テキスト入力',
            'text_output': 'テキスト出力',
            'enter_text': 'テキストを入力...',
            'converted_text': '変換されたテキスト...',
            'key_management': '鍵管理',
            'generate_keys': '鍵を生成',
            'load_private_key': '秘密鍵を読み込む',
            'load_public_key': '公開鍵を読み込む',
            'keys_not_loaded': '鍵：読み込まれていません',
            'private_key': '秘密鍵',
            'public_key': '公開鍵',
            'plaintext': '平文',
            'ciphertext': '暗号文（16進数）',
            'enter_plaintext': '平文を入力...',
            'encrypted_hex': '暗号化された16進数テキスト...',
            'encrypt': '暗号化 →',
            'decrypt': '← 復号化',
            'file': 'ファイル(&F)',
            'quit': '終了',
            'language': '言語(&L)',
            'help': 'ヘルプ(&H)',
            'github': 'GitHubリポジトリ',
            'check_version': 'バージョン確認',
            'about': 'について',
            'confirm': '確認',
            'keys_exist': '鍵が既に存在します。新しい鍵を生成しますか？',
            'yes': 'はい',
            'no': 'いいえ',
            'success': '成功',
            'keys_generated': '鍵が生成されました！\n\n秘密鍵：{}\n公開鍵：{}',
            'error': 'エラー',
            'failed_generate_keys': '鍵の生成に失敗：\n{}',
            'warning': '警告',
            'load_public_first': '公開鍵を先に読み込んでください。',
            'no_plaintext': '暗号化する平文がありません。',
            'no_ciphertext': '復号化する暗号文がありません。',
            'public_key_not_found': '公開鍵ファイルが見つかりません。',
            'private_key_not_found': '秘密鍵ファイルが見つかりません。',
            'encryption_failed': '暗号化に失敗：\n{}',
            'decryption_failed': '復号化に失敗：\n{}',
            'invalid_hex': '無効な16進数文字列です。',
            'load_private_first': '秘密鍵を先に読み込んでください。',
            'save_private_key': '秘密鍵を保存',
            'save_public_key': '公開鍵を保存',
            'open_private_key': '秘密鍵を開く',
            'open_public_key': '公開鍵を開く',
            'pem_files': 'PEMファイル (*.pem);;すべてのファイル (*)',
            'version': 'バージョン',
            'current_remote': '現在：v{}\n最新：v{}\n\nリリース：{}',
            'network_error': 'ネットワークエラー',
            'could_not_check': '更新を確認できません。\n\n現在のバージョン：v{}',
            'about_text': 'EchoRev v{}\nリリース：{}\n\nテキスト方向反転とRSA暗号化ツール。\n\nhttps://github.com/cycleuser/EchoRev',
            'status_bar': 'EchoRev v{} | リリース：{}',
        },
        'fr': {
            'app_title': 'EchoRev',
            'tab_text_direction': 'Direction du texte',
            'tab_encryption': 'Chiffrement / Déchiffrement',
            'direction_mode': 'Mode de direction',
            'horizontal_reverse': 'Inverser horizontalement',
            'vertical_lr': 'Vertical G→D',
            'traditional_chinese': 'Chinois traditionnel',
            'text_input': 'Entrée de texte',
            'text_output': 'Sortie de texte',
            'enter_text': 'Entrez le texte ici...',
            'converted_text': 'Texte converti...',
            'key_management': 'Gestion des clés',
            'generate_keys': 'Générer les clés',
            'load_private_key': 'Charger clé privée',
            'load_public_key': 'Charger clé publique',
            'keys_not_loaded': 'Clés : Non chargées',
            'private_key': 'Clé privée',
            'public_key': 'Clé publique',
            'plaintext': 'Texte en clair',
            'ciphertext': 'Texte chiffré (Hex)',
            'enter_plaintext': 'Entrez le texte en clair...',
            'encrypted_hex': 'Texte hex chiffré...',
            'encrypt': 'Chiffrer →',
            'decrypt': '← Déchiffrer',
            'file': '&Fichier',
            'quit': 'Quitter',
            'language': '&Langue',
            'help': '&Aide',
            'github': 'Dépôt GitHub',
            'check_version': 'Vérifier version',
            'about': 'À propos',
            'confirm': 'Confirmer',
            'keys_exist': 'Les clés existent déjà. Générer de nouvelles clés ?',
            'yes': 'Oui',
            'no': 'Non',
            'success': 'Succès',
            'keys_generated': 'Clés générées !\n\nPrivée : {}\nPublique : {}',
            'error': 'Erreur',
            'failed_generate_keys': 'Échec de génération des clés :\n{}',
            'warning': 'Avertissement',
            'load_public_first': 'Veuillez charger une clé publique.',
            'no_plaintext': 'Pas de texte à chiffrer.',
            'no_ciphertext': 'Pas de texte à déchiffrer.',
            'public_key_not_found': 'Fichier clé publique introuvable.',
            'private_key_not_found': 'Fichier clé privée introuvable.',
            'encryption_failed': 'Échec du chiffrement :\n{}',
            'decryption_failed': 'Échec du déchiffrement :\n{}',
            'invalid_hex': 'Chaîne hex invalide.',
            'load_private_first': 'Veuillez charger une clé privée.',
            'save_private_key': 'Enregistrer clé privée',
            'save_public_key': 'Enregistrer clé publique',
            'open_private_key': 'Ouvrir clé privée',
            'open_public_key': 'Ouvrir clé publique',
            'pem_files': 'Fichiers PEM (*.pem);;Tous les fichiers (*)',
            'version': 'Version',
            'current_remote': 'Actuelle : v{}\nDernière : v{}\n\nPubliée : {}',
            'network_error': 'Erreur réseau',
            'could_not_check': 'Impossible de vérifier les mises à jour.\n\nVersion actuelle : v{}',
            'about_text': 'EchoRev v{}\nPublié : {}\n\nOutil d\'inversion de texte et chiffrement RSA.\n\nhttps://github.com/cycleuser/EchoRev',
            'status_bar': 'EchoRev v{} | Publié : {}',
        },
        'ru': {
            'app_title': 'EchoRev',
            'tab_text_direction': 'Направление текста',
            'tab_encryption': 'Шифрование / Расшифровка',
            'direction_mode': 'Режим направления',
            'horizontal_reverse': 'Горизонтальное отражение',
            'vertical_lr': 'Вертикально Л→П',
            'traditional_chinese': 'Традиционный китайский',
            'text_input': 'Ввод текста',
            'text_output': 'Вывод текста',
            'enter_text': 'Введите текст...',
            'converted_text': 'Преобразованный текст...',
            'key_management': 'Управление ключами',
            'generate_keys': 'Создать ключи',
            'load_private_key': 'Загрузить закрытый ключ',
            'load_public_key': 'Загрузить открытый ключ',
            'keys_not_loaded': 'Ключи: Не загружены',
            'private_key': 'Закрытый ключ',
            'public_key': 'Открытый ключ',
            'plaintext': 'Открытый текст',
            'ciphertext': 'Зашифрованный (Hex)',
            'enter_plaintext': 'Введите открытый текст...',
            'encrypted_hex': 'Зашифрованный hex-текст...',
            'encrypt': 'Зашифровать →',
            'decrypt': '← Расшифровать',
            'file': '&Файл',
            'quit': 'Выход',
            'language': '&Язык',
            'help': '&Справка',
            'github': 'Репозиторий GitHub',
            'check_version': 'Проверить версию',
            'about': 'О программе',
            'confirm': 'Подтверждение',
            'keys_exist': 'Ключи уже существуют. Создать новые?',
            'yes': 'Да',
            'no': 'Нет',
            'success': 'Успех',
            'keys_generated': 'Ключи созданы!\n\nЗакрытый: {}\nОткрытый: {}',
            'error': 'Ошибка',
            'failed_generate_keys': 'Ошибка создания ключей:\n{}',
            'warning': 'Предупреждение',
            'load_public_first': 'Пожалуйста, загрузите открытый ключ.',
            'no_plaintext': 'Нет текста для шифрования.',
            'no_ciphertext': 'Нет текста для расшифровки.',
            'public_key_not_found': 'Файл открытого ключа не найден.',
            'private_key_not_found': 'Файл закрытого ключа не найден.',
            'encryption_failed': 'Ошибка шифрования:\n{}',
            'decryption_failed': 'Ошибка расшифровки:\n{}',
            'invalid_hex': 'Неверная hex-строка.',
            'load_private_first': 'Пожалуйста, загрузите закрытый ключ.',
            'save_private_key': 'Сохранить закрытый ключ',
            'save_public_key': 'Сохранить открытый ключ',
            'open_private_key': 'Открыть закрытый ключ',
            'open_public_key': 'Открыть открытый ключ',
            'pem_files': 'PEM файлы (*.pem);;Все файлы (*)',
            'version': 'Версия',
            'current_remote': 'Текущая: v{}\nПоследняя: v{}\n\nОпубликовано: {}',
            'network_error': 'Ошибка сети',
            'could_not_check': 'Не удалось проверить обновления.\n\nТекущая версия: v{}',
            'about_text': 'EchoRev v{}\nОпубликовано: {}\n\nИнструмент для инверсии текста и RSA шифрования.\n\nhttps://github.com/cycleuser/EchoRev',
            'status_bar': 'EchoRev v{} | Опубликовано: {}',
        },
        'de': {
            'app_title': 'EchoRev',
            'tab_text_direction': 'Textrichtung',
            'tab_encryption': 'Verschlüsselung / Entschlüsselung',
            'direction_mode': 'Richtungsmodus',
            'horizontal_reverse': 'Horizontal umkehren',
            'vertical_lr': 'Vertikal L→R',
            'traditional_chinese': 'Traditionelles Chinesisch',
            'text_input': 'Texteingabe',
            'text_output': 'Textausgabe',
            'enter_text': 'Text eingeben...',
            'converted_text': 'Konvertierter Text...',
            'key_management': 'Schlüsselverwaltung',
            'generate_keys': 'Schlüssel generieren',
            'load_private_key': 'Privaten Schlüssel laden',
            'load_public_key': 'Öffentlichen Schlüssel laden',
            'keys_not_loaded': 'Schlüssel: Nicht geladen',
            'private_key': 'Privater Schlüssel',
            'public_key': 'Öffentlicher Schlüssel',
            'plaintext': 'Klartext',
            'ciphertext': 'Chiffretext (Hex)',
            'enter_plaintext': 'Klartext eingeben...',
            'encrypted_hex': 'Verschlüsselter Hex-Text...',
            'encrypt': 'Verschlüsseln →',
            'decrypt': '← Entschlüsseln',
            'file': '&Datei',
            'quit': 'Beenden',
            'language': '&Sprache',
            'help': '&Hilfe',
            'github': 'GitHub Repository',
            'check_version': 'Version prüfen',
            'about': 'Über',
            'confirm': 'Bestätigen',
            'keys_exist': 'Schlüssel existieren bereits. Neue generieren?',
            'yes': 'Ja',
            'no': 'Nein',
            'success': 'Erfolg',
            'keys_generated': 'Schlüssel generiert!\n\nPrivat: {}\nÖffentlich: {}',
            'error': 'Fehler',
            'failed_generate_keys': 'Fehler beim Generieren:\n{}',
            'warning': 'Warnung',
            'load_public_first': 'Bitte laden Sie einen öffentlichen Schlüssel.',
            'no_plaintext': 'Kein Text zum Verschlüsseln.',
            'no_ciphertext': 'Kein Text zum Entschlüsseln.',
            'public_key_not_found': 'Öffentliche Schlüsseldatei nicht gefunden.',
            'private_key_not_found': 'Private Schlüsseldatei nicht gefunden.',
            'encryption_failed': 'Verschlüsselung fehlgeschlagen:\n{}',
            'decryption_failed': 'Entschlüsselung fehlgeschlagen:\n{}',
            'invalid_hex': 'Ungültige Hex-Zeichenfolge.',
            'load_private_first': 'Bitte laden Sie einen privaten Schlüssel.',
            'save_private_key': 'Privaten Schlüssel speichern',
            'save_public_key': 'Öffentlichen Schlüssel speichern',
            'open_private_key': 'Privaten Schlüssel öffnen',
            'open_public_key': 'Öffentlichen Schlüssel öffnen',
            'pem_files': 'PEM Dateien (*.pem);;Alle Dateien (*)',
            'version': 'Version',
            'current_remote': 'Aktuell: v{}\nNeueste: v{}\n\nVeröffentlicht: {}',
            'network_error': 'Netzwerkfehler',
            'could_not_check': 'Konnte nicht nach Updates suchen.\n\nAktuelle Version: v{}',
            'about_text': 'EchoRev v{}\nVeröffentlicht: {}\n\nTextumkehrungs- und RSA-Verschlüsselungstool.\n\nhttps://github.com/cycleuser/EchoRev',
            'status_bar': 'EchoRev v{} | Veröffentlicht: {}',
        },
        'it': {
            'app_title': 'EchoRev',
            'tab_text_direction': 'Direzione testo',
            'tab_encryption': 'Crittografia / Decrittografia',
            'direction_mode': 'Modalità direzione',
            'horizontal_reverse': 'Inversione orizzontale',
            'vertical_lr': 'Verticale S→D',
            'traditional_chinese': 'Cinese tradizionale',
            'text_input': 'Input testo',
            'text_output': 'Output testo',
            'enter_text': 'Inserisci testo...',
            'converted_text': 'Testo convertito...',
            'key_management': 'Gestione chiavi',
            'generate_keys': 'Genera chiavi',
            'load_private_key': 'Carica chiave privata',
            'load_public_key': 'Carica chiave pubblica',
            'keys_not_loaded': 'Chiavi: Non caricate',
            'private_key': 'Chiave privata',
            'public_key': 'Chiave pubblica',
            'plaintext': 'Testo in chiaro',
            'ciphertext': 'Testo cifrato (Hex)',
            'enter_plaintext': 'Inserisci testo in chiaro...',
            'encrypted_hex': 'Testo hex cifrato...',
            'encrypt': 'Cifra →',
            'decrypt': '← Decifra',
            'file': '&File',
            'quit': 'Esci',
            'language': '&Lingua',
            'help': '&Aiuto',
            'github': 'Repository GitHub',
            'check_version': 'Controlla versione',
            'about': 'Informazioni',
            'confirm': 'Conferma',
            'keys_exist': 'Le chiavi esistono già. Generare nuove chiavi?',
            'yes': 'Sì',
            'no': 'No',
            'success': 'Successo',
            'keys_generated': 'Chiavi generate!\n\nPrivata: {}\nPubblica: {}',
            'error': 'Errore',
            'failed_generate_keys': 'Generazione chiavi fallita:\n{}',
            'warning': 'Avviso',
            'load_public_first': 'Carica prima una chiave pubblica.',
            'no_plaintext': 'Nessun testo da cifrare.',
            'no_ciphertext': 'Nessun testo da decifrare.',
            'public_key_not_found': 'File chiave pubblica non trovato.',
            'private_key_not_found': 'File chiave privata non trovato.',
            'encryption_failed': 'Crittografia fallita:\n{}',
            'decryption_failed': 'Decrittografia fallita:\n{}',
            'invalid_hex': 'Stringa hex non valida.',
            'load_private_first': 'Carica prima una chiave privata.',
            'save_private_key': 'Salva chiave privata',
            'save_public_key': 'Salva chiave pubblica',
            'open_private_key': 'Apri chiave privata',
            'open_public_key': 'Apri chiave pubblica',
            'pem_files': 'File PEM (*.pem);;Tutti i file (*)',
            'version': 'Versione',
            'current_remote': 'Attuale: v{}\nUltima: v{}\n\nPubblicata: {}',
            'network_error': 'Errore di rete',
            'could_not_check': 'Impossibile verificare aggiornamenti.\n\nVersione attuale: v{}',
            'about_text': 'EchoRev v{}\nPubblicato: {}\n\nStrumento per inversione testo e crittografia RSA.\n\nhttps://github.com/cycleuser/EchoRev',
            'status_bar': 'EchoRev v{} | Pubblicato: {}',
        },
        'es': {
            'app_title': 'EchoRev',
            'tab_text_direction': 'Dirección del texto',
            'tab_encryption': 'Cifrado / Descifrado',
            'direction_mode': 'Modo de dirección',
            'horizontal_reverse': 'Invertir horizontal',
            'vertical_lr': 'Vertical I→D',
            'traditional_chinese': 'Chino tradicional',
            'text_input': 'Entrada de texto',
            'text_output': 'Salida de texto',
            'enter_text': 'Ingrese texto...',
            'converted_text': 'Texto convertido...',
            'key_management': 'Gestión de claves',
            'generate_keys': 'Generar claves',
            'load_private_key': 'Cargar clave privada',
            'load_public_key': 'Cargar clave pública',
            'keys_not_loaded': 'Claves: No cargadas',
            'private_key': 'Clave privada',
            'public_key': 'Clave pública',
            'plaintext': 'Texto plano',
            'ciphertext': 'Texto cifrado (Hex)',
            'enter_plaintext': 'Ingrese texto plano...',
            'encrypted_hex': 'Texto hex cifrado...',
            'encrypt': 'Cifrar →',
            'decrypt': '← Descifrar',
            'file': '&Archivo',
            'quit': 'Salir',
            'language': '&Idioma',
            'help': '&Ayuda',
            'github': 'Repositorio GitHub',
            'check_version': 'Verificar versión',
            'about': 'Acerca de',
            'confirm': 'Confirmar',
            'keys_exist': 'Las claves ya existen. ¿Generar nuevas?',
            'yes': 'Sí',
            'no': 'No',
            'success': 'Éxito',
            'keys_generated': '¡Claves generadas!\n\nPrivada: {}\nPública: {}',
            'error': 'Error',
            'failed_generate_keys': 'Error al generar claves:\n{}',
            'warning': 'Advertencia',
            'load_public_first': 'Por favor cargue una clave pública.',
            'no_plaintext': 'No hay texto para cifrar.',
            'no_ciphertext': 'No hay texto para descifrar.',
            'public_key_not_found': 'Archivo de clave pública no encontrado.',
            'private_key_not_found': 'Archivo de clave privada no encontrado.',
            'encryption_failed': 'Cifrado fallido:\n{}',
            'decryption_failed': 'Descifrado fallido:\n{}',
            'invalid_hex': 'Cadena hex inválida.',
            'load_private_first': 'Por favor cargue una clave privada.',
            'save_private_key': 'Guardar clave privada',
            'save_public_key': 'Guardar clave pública',
            'open_private_key': 'Abrir clave privada',
            'open_public_key': 'Abrir clave pública',
            'pem_files': 'Archivos PEM (*.pem);;Todos los archivos (*)',
            'version': 'Versión',
            'current_remote': 'Actual: v{}\nÚltima: v{}\n\nPublicada: {}',
            'network_error': 'Error de red',
            'could_not_check': 'No se pudo verificar actualizaciones.\n\nVersión actual: v{}',
            'about_text': 'EchoRev v{}\nPublicado: {}\n\nHerramienta de inversión de texto y cifrado RSA.\n\nhttps://github.com/cycleuser/EchoRev',
            'status_bar': 'EchoRev v{} | Publicado: {}',
        },
        'pt': {
            'app_title': 'EchoRev',
            'tab_text_direction': 'Direção do texto',
            'tab_encryption': 'Criptografia / Descriptografia',
            'direction_mode': 'Modo de direção',
            'horizontal_reverse': 'Inverter horizontal',
            'vertical_lr': 'Vertical E→D',
            'traditional_chinese': 'Chinês tradicional',
            'text_input': 'Entrada de texto',
            'text_output': 'Saída de texto',
            'enter_text': 'Digite o texto...',
            'converted_text': 'Texto convertido...',
            'key_management': 'Gerenciamento de chaves',
            'generate_keys': 'Gerar chaves',
            'load_private_key': 'Carregar chave privada',
            'load_public_key': 'Carregar chave pública',
            'keys_not_loaded': 'Chaves: Não carregadas',
            'private_key': 'Chave privada',
            'public_key': 'Chave pública',
            'plaintext': 'Texto simples',
            'ciphertext': 'Texto cifrado (Hex)',
            'enter_plaintext': 'Digite o texto simples...',
            'encrypted_hex': 'Texto hex cifrado...',
            'encrypt': 'Cifrar →',
            'decrypt': '← Decifrar',
            'file': '&Arquivo',
            'quit': 'Sair',
            'language': '&Idioma',
            'help': '&Ajuda',
            'github': 'Repositório GitHub',
            'check_version': 'Verificar versão',
            'about': 'Sobre',
            'confirm': 'Confirmar',
            'keys_exist': 'As chaves já existem. Gerar novas chaves?',
            'yes': 'Sim',
            'no': 'Não',
            'success': 'Sucesso',
            'keys_generated': 'Chaves geradas!\n\nPrivada: {}\nPública: {}',
            'error': 'Erro',
            'failed_generate_keys': 'Falha ao gerar chaves:\n{}',
            'warning': 'Aviso',
            'load_public_first': 'Por favor carregue uma chave pública.',
            'no_plaintext': 'Sem texto para cifrar.',
            'no_ciphertext': 'Sem texto para decifrar.',
            'public_key_not_found': 'Arquivo de chave pública não encontrado.',
            'private_key_not_found': 'Arquivo de chave privada não encontrado.',
            'encryption_failed': 'Criptografia falhou:\n{}',
            'decryption_failed': 'Descriptografia falhou:\n{}',
            'invalid_hex': 'String hex inválida.',
            'load_private_first': 'Por favor carregue uma chave privada.',
            'save_private_key': 'Salvar chave privada',
            'save_public_key': 'Salvar chave pública',
            'open_private_key': 'Abrir chave privada',
            'open_public_key': 'Abrir chave pública',
            'pem_files': 'Arquivos PEM (*.pem);;Todos os arquivos (*)',
            'version': 'Versão',
            'current_remote': 'Atual: v{}\nÚltima: v{}\n\nPublicada: {}',
            'network_error': 'Erro de rede',
            'could_not_check': 'Não foi possível verificar atualizações.\n\nVersão atual: v{}',
            'about_text': 'EchoRev v{}\nPublicado: {}\n\nFerramenta de inversão de texto e criptografia RSA.\n\nhttps://github.com/cycleuser/EchoRev',
            'status_bar': 'EchoRev v{} | Publicado: {}',
        },
        'ko': {
            'app_title': 'EchoRev',
            'tab_text_direction': '텍스트 방향',
            'tab_encryption': '암호화 / 복호화',
            'direction_mode': '방향 모드',
            'horizontal_reverse': '수평 반전',
            'vertical_lr': '수직 L→R',
            'traditional_chinese': '번체 중국어',
            'text_input': '텍스트 입력',
            'text_output': '텍스트 출력',
            'enter_text': '텍스트 입력...',
            'converted_text': '변환된 텍스트...',
            'key_management': '키 관리',
            'generate_keys': '키 생성',
            'load_private_key': '개인 키 로드',
            'load_public_key': '공개 키 로드',
            'keys_not_loaded': '키: 로드되지 않음',
            'private_key': '개인 키',
            'public_key': '공개 키',
            'plaintext': '평문',
            'ciphertext': '암호문 (Hex)',
            'enter_plaintext': '평문 입력...',
            'encrypted_hex': '암호화된 hex 텍스트...',
            'encrypt': '암호화 →',
            'decrypt': '← 복호화',
            'file': '파일(&F)',
            'quit': '종료',
            'language': '언어(&L)',
            'help': '도움말(&H)',
            'github': 'GitHub 저장소',
            'check_version': '버전 확인',
            'about': '정보',
            'confirm': '확인',
            'keys_exist': '키가 이미 존재합니다. 새 키를 생성하시겠습니까?',
            'yes': '예',
            'no': '아니요',
            'success': '성공',
            'keys_generated': '키가 생성되었습니다!\n\n개인 키: {}\n공개 키: {}',
            'error': '오류',
            'failed_generate_keys': '키 생성 실패:\n{}',
            'warning': '경고',
            'load_public_first': '공개 키를 먼저 로드하세요.',
            'no_plaintext': '암호화할 평문이 없습니다.',
            'no_ciphertext': '복호화할 암호문이 없습니다.',
            'public_key_not_found': '공개 키 파일을 찾을 수 없습니다.',
            'private_key_not_found': '개인 키 파일을 찾을 수 없습니다.',
            'encryption_failed': '암호화 실패:\n{}',
            'decryption_failed': '복호화 실패:\n{}',
            'invalid_hex': '잘못된 hex 문자열입니다.',
            'load_private_first': '개인 키를 먼저 로드하세요.',
            'save_private_key': '개인 키 저장',
            'save_public_key': '공개 키 저장',
            'open_private_key': '개인 키 열기',
            'open_public_key': '공개 키 열기',
            'pem_files': 'PEM 파일 (*.pem);;모든 파일 (*)',
            'version': '버전',
            'current_remote': '현재: v{}\n최신: v{}\n\n출시: {}',
            'network_error': '네트워크 오류',
            'could_not_check': '업데이트를 확인할 수 없습니다.\n\n현재 버전: v{}',
            'about_text': 'EchoRev v{}\n출시: {}\n\n텍스트 방향 반전 및 RSA 암호화 도구.\n\nhttps://github.com/cycleuser/EchoRev',
            'status_bar': 'EchoRev v{} | 출시: {}',
        },
    }
    
    _current_lang = 'en'
    _callbacks = []
    
    @classmethod
    def set_language(cls, lang: str):
        if lang in cls.TRANSLATIONS:
            cls._current_lang = lang
            for callback in cls._callbacks:
                callback()
    
    @classmethod
    def get_language(cls) -> str:
        return cls._current_lang
    
    @classmethod
    def register_callback(cls, callback):
        cls._callbacks.append(callback)
    
    @classmethod
    def t(cls, key: str) -> str:
        return cls.TRANSLATIONS.get(cls._current_lang, {}).get(key, key)
    
    @classmethod
    def detect_system_language(cls) -> str:
        locale_map = {
            'zh': 'zh', 'ja': 'ja', 'fr': 'fr', 'ru': 'ru',
            'de': 'de', 'it': 'it', 'es': 'es', 'pt': 'pt', 'ko': 'ko',
        }
        sys_lang = QLocale.system().name()[:2]
        return locale_map.get(sys_lang, 'en')


class WatermarkTextEdit(QTextEdit):
    """Text editor with watermark support."""
    
    def __init__(self, watermark_key: str, parent=None):
        super().__init__(parent)
        self._watermark_key = watermark_key
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        I18N.register_callback(self._update_watermark)
    
    def _update_watermark(self):
        self.update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        if self._watermark_key and not self.toPlainText():
            painter = QPainter(self.viewport())
            painter.setPen(QColor(180, 180, 180, 150))
            painter.setFont(QFont("Arial", 16))
            painter.drawText(self.rect(), Qt.AlignCenter, I18N.t(self._watermark_key))
            painter.end()


class TextReverseWidget(QWidget):
    """Widget for text direction reversal."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        I18N.register_callback(self._retranslate_ui)
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        control_group = QGroupBox()
        control_layout = QHBoxLayout(control_group)
        self._control_group = control_group
        
        self._slider = QSlider(Qt.Horizontal)
        self._slider.setRange(0, 2)
        self._slider.setValue(0)
        self._slider.setTickPosition(QSlider.TicksBelow)
        self._slider.setTickInterval(1)
        self._slider.valueChanged.connect(self._on_slider_changed)
        control_layout.addWidget(self._slider, 1)
        
        self._mode_label = QLabel()
        self._mode_label.setMinimumWidth(150)
        control_layout.addWidget(self._mode_label)
        
        layout.addWidget(control_group)
        
        self._mode_labels_layout = QHBoxLayout()
        self._mode_labels = []
        for key in ['horizontal_reverse', 'vertical_lr', 'traditional_chinese']:
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            self._mode_labels.append(label)
            self._mode_labels_layout.addWidget(label)
        layout.addLayout(self._mode_labels_layout)
        
        text_layout = QHBoxLayout()
        
        input_group = QGroupBox()
        self._input_group = input_group
        input_layout = QVBoxLayout(input_group)
        self._text_input = WatermarkTextEdit('enter_text')
        self._text_input.textChanged.connect(self._on_text_changed)
        input_layout.addWidget(self._text_input)
        text_layout.addWidget(input_group)
        
        output_group = QGroupBox()
        self._output_group = output_group
        output_layout = QVBoxLayout(output_group)
        self._text_output = WatermarkTextEdit('converted_text')
        self._text_output.setReadOnly(True)
        output_layout.addWidget(self._text_output)
        text_layout.addWidget(output_group)
        
        layout.addLayout(text_layout, 1)
        self._retranslate_ui()
    
    def _retranslate_ui(self):
        self._control_group.setTitle(I18N.t('direction_mode'))
        self._input_group.setTitle(I18N.t('text_input'))
        self._output_group.setTitle(I18N.t('text_output'))
        
        modes = ['horizontal_reverse', 'vertical_lr', 'traditional_chinese']
        self._mode_label.setText(I18N.t(modes[self._slider.value()]))
        for i, label in enumerate(self._mode_labels):
            label.setText(I18N.t(modes[i]))
    
    def _on_slider_changed(self, value: int):
        modes = ['horizontal_reverse', 'vertical_lr', 'traditional_chinese']
        self._mode_label.setText(I18N.t(modes[value]))
        self._on_text_changed()
    
    def _is_chinese(self, text: str) -> bool:
        return any('\u4e00' <= char <= '\u9fff' for char in text)
    
    def _on_text_changed(self):
        input_text = self._text_input.toPlainText()
        if not input_text:
            self._text_output.clear()
            return
        
        slider_value = self._slider.value()
        lines = input_text.split('\n')
        
        if slider_value == 0:
            result_lines = [line[::-1] for line in lines]
        else:
            max_len = max((len(line) for line in lines), default=0)
            result_lines = []
            
            for i in range(max_len):
                chars = []
                for line in lines:
                    if i < len(line):
                        chars.append(line[i])
                    else:
                        fill_char = '\u3000' if self._is_chinese(input_text) else ' '
                        chars.append(fill_char)
                
                column = ''.join(chars)
                if slider_value == 2:
                    column = column[::-1]
                result_lines.append(column)
        
        self._text_output.setPlainText('\n'.join(result_lines))


class CryptoWidget(QWidget):
    """Widget for RSA encryption/decryption."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._private_key_path: str = ''
        self._public_key_path: str = ''
        self._setup_ui()
        I18N.register_callback(self._retranslate_ui)
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        keys_group = QGroupBox()
        self._keys_group = keys_group
        keys_layout = QVBoxLayout(keys_group)
        
        row1 = QHBoxLayout()
        self._btn_generate = QPushButton()
        self._btn_generate.clicked.connect(self._generate_keys)
        row1.addWidget(self._btn_generate)
        
        self._btn_load_private = QPushButton()
        self._btn_load_private.clicked.connect(self._load_private_key)
        row1.addWidget(self._btn_load_private)
        
        self._btn_load_public = QPushButton()
        self._btn_load_public.clicked.connect(self._load_public_key)
        row1.addWidget(self._btn_load_public)
        keys_layout.addLayout(row1)
        
        self._key_status = QLabel()
        keys_layout.addWidget(self._key_status)
        
        layout.addWidget(keys_group)
        
        text_layout = QHBoxLayout()
        
        plain_group = QGroupBox()
        self._plain_group = plain_group
        plain_layout = QVBoxLayout(plain_group)
        self._text_plain = WatermarkTextEdit('enter_plaintext')
        plain_layout.addWidget(self._text_plain)
        
        self._btn_encrypt = QPushButton()
        self._btn_encrypt.clicked.connect(self._encrypt)
        plain_layout.addWidget(self._btn_encrypt)
        
        text_layout.addWidget(plain_group)
        
        cipher_group = QGroupBox()
        self._cipher_group = cipher_group
        cipher_layout = QVBoxLayout(cipher_group)
        self._text_cipher = WatermarkTextEdit('encrypted_hex')
        cipher_layout.addWidget(self._text_cipher)
        
        self._btn_decrypt = QPushButton()
        self._btn_decrypt.clicked.connect(self._decrypt)
        cipher_layout.addWidget(self._btn_decrypt)
        
        text_layout.addWidget(cipher_group)
        
        layout.addLayout(text_layout, 1)
        self._retranslate_ui()
    
    def _retranslate_ui(self):
        self._keys_group.setTitle(I18N.t('key_management'))
        self._btn_generate.setText(I18N.t('generate_keys'))
        self._btn_load_private.setText(I18N.t('load_private_key'))
        self._btn_load_public.setText(I18N.t('load_public_key'))
        self._plain_group.setTitle(I18N.t('plaintext'))
        self._cipher_group.setTitle(I18N.t('ciphertext'))
        self._btn_encrypt.setText(I18N.t('encrypt'))
        self._btn_decrypt.setText(I18N.t('decrypt'))
        self._update_key_status()
    
    def _update_key_status(self):
        if self._private_key_path or self._public_key_path:
            private_name = Path(self._private_key_path).name if self._private_key_path else "-"
            public_name = Path(self._public_key_path).name if self._public_key_path else "-"
            self._key_status.setText(f"{I18N.t('private_key')}: {private_name} | {I18N.t('public_key')}: {public_name}")
        else:
            self._key_status.setText(I18N.t('keys_not_loaded'))
    
    def _generate_keys(self):
        if self._private_key_path or self._public_key_path:
            reply = QMessageBox.question(
                self, I18N.t('confirm'),
                I18N.t('keys_exist'),
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        options = QFileDialog.Options()
        file_filter = I18N.t('pem_files')
        
        private_path, _ = QFileDialog.getSaveFileName(
            self, I18N.t('save_private_key'), "private_key.pem", file_filter, options=options
        )
        if not private_path:
            return
        
        public_path, _ = QFileDialog.getSaveFileName(
            self, I18N.t('save_public_key'), "public_key.pem", file_filter, options=options
        )
        if not public_path:
            return
        
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            public_key = private_key.public_key()
            
            with open(private_path, 'wb') as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            with open(public_path, 'wb') as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
            
            self._private_key_path = private_path
            self._public_key_path = public_path
            self._update_key_status()
            
            QMessageBox.information(
                self, I18N.t('success'),
                I18N.t('keys_generated').format(private_path, public_path)
            )
        except Exception as e:
            QMessageBox.critical(self, I18N.t('error'), I18N.t('failed_generate_keys').format(str(e)))
    
    def _load_private_key(self):
        path, _ = QFileDialog.getOpenFileName(
            self, I18N.t('open_private_key'), "", I18N.t('pem_files')
        )
        if path:
            self._private_key_path = path
            self._update_key_status()
    
    def _load_public_key(self):
        path, _ = QFileDialog.getOpenFileName(
            self, I18N.t('open_public_key'), "", I18N.t('pem_files')
        )
        if path:
            self._public_key_path = path
            self._update_key_status()
    
    def _encrypt(self):
        if not self._public_key_path:
            QMessageBox.warning(self, I18N.t('warning'), I18N.t('load_public_first'))
            return
        
        plaintext = self._text_plain.toPlainText()
        if not plaintext:
            QMessageBox.warning(self, I18N.t('warning'), I18N.t('no_plaintext'))
            return
        
        try:
            with open(self._public_key_path, 'rb') as f:
                public_key = serialization.load_pem_public_key(
                    f.read(), backend=default_backend()
                )
            
            chunk_size = 190
            encrypted_chunks = []
            
            for i in range(0, len(plaintext), chunk_size):
                chunk = plaintext[i:i + chunk_size].encode('utf-8')
                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                encrypted_chunks.append(encrypted_chunk)
            
            ciphertext = b''.join(encrypted_chunks).hex()
            self._text_cipher.setPlainText(ciphertext)
            
        except FileNotFoundError:
            QMessageBox.critical(self, I18N.t('error'), I18N.t('public_key_not_found'))
        except Exception as e:
            QMessageBox.critical(self, I18N.t('error'), I18N.t('encryption_failed').format(str(e)))
    
    def _decrypt(self):
        if not self._private_key_path:
            QMessageBox.warning(self, I18N.t('warning'), I18N.t('load_private_first'))
            return
        
        ciphertext_hex = self._text_cipher.toPlainText()
        if not ciphertext_hex:
            QMessageBox.warning(self, I18N.t('warning'), I18N.t('no_ciphertext'))
            return
        
        try:
            ciphertext = bytes.fromhex(ciphertext_hex.strip())
        except ValueError:
            QMessageBox.critical(self, I18N.t('error'), I18N.t('invalid_hex'))
            return
        
        try:
            with open(self._private_key_path, 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(), password=None, backend=default_backend()
                )
            
            chunk_size = 256
            decrypted_chunks = []
            
            for i in range(0, len(ciphertext), chunk_size):
                chunk = ciphertext[i:i + chunk_size]
                decrypted_chunk = private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                decrypted_chunks.append(decrypted_chunk)
            
            plaintext = b''.join(decrypted_chunks).decode('utf-8')
            self._text_plain.setPlainText(plaintext)
            
        except FileNotFoundError:
            QMessageBox.critical(self, I18N.t('error'), I18N.t('private_key_not_found'))
        except Exception as e:
            QMessageBox.critical(self, I18N.t('error'), I18N.t('decryption_failed').format(str(e)))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        I18N.register_callback(self._retranslate_ui)
        I18N.set_language(I18N.detect_system_language())
    
    def _setup_ui(self):
        self.setObjectName('MainWindow')
        self.setMinimumSize(800, 600)
        self.resize(900, 650)
        
        icon_path = LOCATION / 'icon.png'
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self._tab_widget = QTabWidget()
        self._text_reverse_widget = TextReverseWidget()
        self._crypto_widget = CryptoWidget()
        self._tab_widget.addTab(self._text_reverse_widget, "")
        self._tab_widget.addTab(self._crypto_widget, "")
        layout.addWidget(self._tab_widget)
        
        self._create_menu()
        self._create_statusbar()
        self._retranslate_ui()
    
    def _create_menu(self):
        menubar = self.menuBar()
        
        self._file_menu = menubar.addMenu("")
        
        self._action_quit = QAction(self)
        self._action_quit.setShortcut('Ctrl+Q')
        self._action_quit.triggered.connect(QApplication.quit)
        self._file_menu.addAction(self._action_quit)
        
        self._lang_menu = menubar.addMenu("")
        self._lang_actions = {}
        for lang_code, lang_name in I18N.LANGUAGES.items():
            action = QAction(lang_name, self)
            action.triggered.connect(lambda checked, l=lang_code: I18N.set_language(l))
            self._lang_menu.addAction(action)
            self._lang_actions[lang_code] = action
        
        self._help_menu = menubar.addMenu("")
        
        self._action_github = QAction(self)
        self._action_github.triggered.connect(lambda: webbrowser.open('https://github.com/cycleuser/EchoRev'))
        self._help_menu.addAction(self._action_github)
        
        self._action_version = QAction(self)
        self._action_version.triggered.connect(self._check_version)
        self._help_menu.addAction(self._action_version)
        
        self._help_menu.addSeparator()
        
        self._action_about = QAction(self)
        self._action_about.triggered.connect(self._show_about)
        self._help_menu.addAction(self._action_about)
    
    def _create_statusbar(self):
        self._statusbar = QStatusBar()
        self.setStatusBar(self._statusbar)
    
    def _retranslate_ui(self):
        self.setWindowTitle(I18N.t('app_title') + f' v{version}')
        self._tab_widget.setTabText(0, I18N.t('tab_text_direction'))
        self._tab_widget.setTabText(1, I18N.t('tab_encryption'))
        
        self._file_menu.setTitle(I18N.t('file'))
        self._action_quit.setText(I18N.t('quit'))
        self._lang_menu.setTitle(I18N.t('language'))
        self._help_menu.setTitle(I18N.t('help'))
        self._action_github.setText(I18N.t('github'))
        self._action_version.setText(I18N.t('check_version'))
        self._action_about.setText(I18N.t('about'))
        
        self._statusbar.showMessage(I18N.t('status_bar').format(version, date))
    
    def _check_version(self):
        try:
            response = requests.get(
                'https://raw.githubusercontent.com/cycleuser/EchoRev/master/echorev/__init__.py',
                timeout=10
            )
            response.raise_for_status()
            
            for line in response.text.splitlines():
                if line.startswith('__version__'):
                    remote_version = line.split('=')[1].strip().strip("'\"")
                    break
            else:
                remote_version = 'unknown'
            
            QMessageBox.information(
                self, I18N.t('version'),
                I18N.t('current_remote').format(version, remote_version, date)
            )
        except Exception:
            QMessageBox.warning(
                self, I18N.t('network_error'),
                I18N.t('could_not_check').format(version)
            )
    
    def _show_about(self):
        QMessageBox.about(
            self, I18N.t('about'),
            I18N.t('about_text').format(version, date)
        )


def main():
    app = QApplication(sys.argv)
    app.installTranslator(QTranslator())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()