---
name: aussie-mortgage-calc
description: Australian mortgage calculator — LVR, stamp duty, LMI, repayments, and First Home Buyer concessions by state.
homepage: https://oneyco.com.au
metadata: {"clawdbot":{"emoji":"🏠","category":"Finance"}}
---

# Australian Mortgage Calculator

Comprehensive mortgage calculations for Australian property buyers. All amounts in AUD.

## Quick Calculations

### LVR (Loan to Value Ratio)
```
LVR = (Loan Amount / Property Value) × 100

Example:
- Property: $800,000
- Loan: $640,000
- LVR: 80%
```

### Monthly Repayment (P&I)
```
M = P × [r(1+r)^n] / [(1+r)^n – 1]

Where:
- P = Principal (loan amount)
- r = Monthly interest rate (annual rate / 12)
- n = Total months (loan term × 12)

Example: $500,000 loan at 6.5% over 30 years
- Monthly rate: 0.065/12 = 0.00542
- Months: 360
- Monthly repayment: $3,160
```

### Interest Only Repayment
```
Monthly IO = Principal × (Annual Rate / 12)

Example: $500,000 at 6.5%
- Monthly IO: $2,708
```

---

## Stamp Duty by State (2024-25)

### NSW (New South Wales)
| Property Value | Duty Rate |
|----------------|-----------|
| $0 – $16,000 | 1.25% |
| $16,001 – $35,000 | $200 + 1.50% of excess |
| $35,001 – $93,000 | $485 + 1.75% of excess |
| $93,001 – $351,000 | $1,500 + 3.50% of excess |
| $351,001 – $1,168,000 | $10,530 + 4.50% of excess |
| Over $1,168,000 | $47,295 + 5.50% of excess |

**First Home Buyer**: Full exemption up to $800,000; concession $800,001-$1,000,000

### VIC (Victoria)
| Property Value | Duty Rate |
|----------------|-----------|
| $0 – $25,000 | 1.4% |
| $25,001 – $130,000 | $350 + 2.4% of excess |
| $130,001 – $960,000 | $2,870 + 6.0% of excess |
| Over $960,000 | 5.5% flat |

**First Home Buyer**: Full exemption up to $600,000; concession $600,001-$750,000

### QLD (Queensland)
| Property Value | Duty Rate |
|----------------|-----------|
| $0 – $350,000 | 1.0% (min $0) |
| $350,001 – $540,000 | $3,500 + 3.5% of excess |
| $540,001 – $1,000,000 | $10,150 + 4.5% of excess |
| Over $1,000,000 | $30,850 + 5.75% of excess |

**First Home Buyer**: Full exemption up to $700,000 (for new homes); concession for established

### WA (Western Australia)
| Property Value | Duty Rate |
|----------------|-----------|
| $0 – $120,000 | 1.9% |
| $120,001 – $150,000 | $2,280 + 2.85% of excess |
| $150,001 – $360,000 | $3,135 + 3.80% of excess |
| $360,001 – $725,000 | $11,115 + 4.75% of excess |
| Over $725,000 | $28,453 + 5.15% of excess |

**First Home Buyer**: Full exemption up to $430,000; concession $430,001-$530,000

### SA (South Australia)
| Property Value | Duty Rate |
|----------------|-----------|
| $0 – $12,000 | 1.0% |
| $12,001 – $30,000 | $120 + 2.0% of excess |
| $30,001 – $50,000 | $480 + 3.0% of excess |
| $50,001 – $100,000 | $1,080 + 3.5% of excess |
| $100,001 – $200,000 | $2,830 + 4.0% of excess |
| $200,001 – $250,000 | $6,830 + 4.25% of excess |
| $250,001 – $300,000 | $8,955 + 4.75% of excess |
| $300,001 – $500,000 | $11,330 + 5.0% of excess |
| Over $500,000 | $21,330 + 5.5% of excess |

**First Home Buyer**: No stamp duty for properties up to $650,000 (eligible buyers)

### TAS (Tasmania)
| Property Value | Duty Rate |
|----------------|-----------|
| $0 – $3,000 | $50 |
| $3,001 – $25,000 | $50 + 1.75% of excess |
| $25,001 – $75,000 | $435 + 2.25% of excess |
| $75,001 – $200,000 | $1,560 + 3.50% of excess |
| $200,001 – $375,000 | $5,935 + 4.00% of excess |
| $375,001 – $725,000 | $12,935 + 4.25% of excess |
| Over $725,000 | $27,810 + 4.50% of excess |

**First Home Buyer**: 50% duty discount for properties up to $600,000

### NT (Northern Territory)
| Property Value | Duty Rate |
|----------------|-----------|
| $0 – $525,000 | V = 0.06571441 × V^2 ÷ 1000 |
| Over $525,000 | 5.45% flat minus $4,823.45 |

**First Home Buyer**: Up to $18,601 discount for properties under $650,000

### ACT (Australian Capital Territory)
| Property Value | Duty Rate |
|----------------|-----------|
| $0 – $260,000 | $0.60 per $100 or part |
| $260,001 – $300,000 | $1,560 + $2.20 per $100 |
| $300,001 – $500,000 | $2,440 + $3.40 per $100 |
| $500,001 – $750,000 | $9,240 + $4.32 per $100 |
| $750,001 – $1,000,000 | $20,040 + $5.90 per $100 |
| $1,000,001 – $1,455,000 | $34,790 + $6.40 per $100 |
| Over $1,455,000 | $63,910 + $4.54 per $100 |

**First Home Buyer**: Full exemption up to $1,000,000 (income-tested)

---

## LMI (Lenders Mortgage Insurance)

LMI is required when LVR > 80%. Estimated rates:

| LVR | LMI as % of Loan |
|-----|------------------|
| 80.01% – 85% | 0.5% – 1.0% |
| 85.01% – 90% | 1.5% – 2.5% |
| 90.01% – 95% | 3.0% – 4.5% |

**Example**: $600,000 loan at 90% LVR
- LMI estimate: ~$12,000 – $15,000 (can be added to loan)

> Note: Actual LMI varies by lender, LVR tier, loan amount, and borrower profile. Use lender calculators for exact quotes.

---

## First Home Owner Grant (FHOG)

| State | Grant Amount | Property Cap |
|-------|--------------|--------------|
| NSW | $10,000 | $600,000 (new homes only) |
| VIC | $10,000 | $750,000 (regional: higher) |
| QLD | $30,000 | $750,000 (new homes only) |
| WA | $10,000 | $750,000 (new homes) |
| SA | $15,000 | $650,000 (new homes only) |
| TAS | $30,000 | $600,000 (new homes only) |
| NT | $10,000 | No cap (new homes) |
| ACT | Abolished | — |

---

## Borrowing Power (Quick Estimate)

Basic rule of thumb:
```
Max Borrowing ≈ (Annual Income × 6) – Existing Debts

More conservative:
Max Borrowing ≈ (Annual Income × 5) – Existing Debts
```

Factors affecting actual borrowing power:
- Income type (PAYG vs self-employed)
- Existing debts (credit cards, HECS, car loans)
- Living expenses (HEM benchmark)
- Interest rate buffer (usually +3%)
- Dependents

---

## Key Contacts

- **Revenue NSW**: revenue.nsw.gov.au
- **State Revenue Victoria**: sro.vic.gov.au
- **Queensland Treasury**: qld.gov.au/housing
- **WA RevenueWA**: wa.gov.au/revenuelicensing
- **RevenueSA**: revenuesa.sa.gov.au
- **Tasmania State Revenue**: treasury.tas.gov.au
- **NT Treasury**: treasury.nt.gov.au
- **ACT Revenue**: revenue.act.gov.au

---

## Disclaimer

This skill provides estimates for educational purposes only. Stamp duty rates, concessions, and grants change periodically. Always verify with official state revenue offices and consult a qualified mortgage broker or financial advisor before making property decisions.

**Built by [Oney & Co](https://oneyco.com.au)** — Helping Australians navigate lending with clarity.
