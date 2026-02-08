---
name: eyebot-lightningbot
description: Manage Lightning Network wallets with LNbits. Check balance, create invoices with QR codes, pay invoices, and manage Bitcoin Lightning payments instantly with near-zero fees.
metadata: {"clawdbot":{"emoji":"⚡","homepage":"https://eyebots.io","requires":{"bins":["python3"],"pip":["qrcode[pil]","requests"]}}}
---

# LightningBot Elite ⚡

**Ultimate Lightning Network Wallet Manager**

Manage LNbits Lightning wallets with instant Bitcoin payments.

## ⚡ Elite Features

### Wallet Management
- Create new LNbits wallets
- Check balance in satoshis
- Secure key management

### Receive Payments
- Generate Bolt11 invoices
- Auto QR code generation
- Custom memo/description

### Send Payments
- Pay Lightning invoices
- Decode invoices before paying
- Balance verification

## Trigger Keywords

```
lightning, bitcoin, btc, sats, satoshis,
lnbits, lightning network, bolt11, invoice,
receive bitcoin, send bitcoin, pay invoice,
lightning wallet, btc wallet, create invoice,
qr code, generate invoice, check balance,
lightning payment, instant payment, ln wallet,
bitcoin wallet, pay btc, receive btc
```

## Usage

### Create Wallet
```bash
python3 scripts/lnbits_cli.py create --name "My Wallet"
```

### Check Balance
```bash
python3 scripts/lnbits_cli.py balance
```

### Create Invoice (Receive)
```bash
python3 scripts/lnbits_cli.py invoice --amount 1000 --memo "Payment"
```

### Pay Invoice (Send)
```bash
python3 scripts/lnbits_cli.py pay <bolt11_invoice>
```

### Decode Invoice
```bash
python3 scripts/lnbits_cli.py decode <bolt11_invoice>
```

## Security Protocols

⚠️ CRITICAL:
- NEVER expose Admin Keys
- Always confirm before paying
- Check balance before sending

## Part of Eye Elite Suite 🔥
