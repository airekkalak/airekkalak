# Vehicle Profile

> Fill in what you know; leave `—` where you don't. Everything here is the
> reference sheet — the moving records live in `data/*.csv`.

## Identity

| Field | Value |
|---|---|
| Nickname | — |
| Make | Honda |
| Model | HR-V |
| Variant / trim | VTi |
| Model year | 2019 |
| Build date | — |
| Body / doors | Wagon (5-door) |
| Colour | Silver |
| VIN | MRHRU5830LP060490 |
| Engine number | — |
| Registration (plate) | 197ZLG |
| State / territory | Queensland |

## Drivetrain

| Field | Value |
|---|---|
| Engine | — |
| Fuel type | — |
| Transmission | — |
| Drive | — |
| Power / torque | — |
| Tank capacity | — |
| Claimed combined economy | — |

## Tyres & wheels

| Field | Value |
|---|---|
| Tyre size (front) | — |
| Tyre size (rear) | — |
| Wheel size / offset | — |
| Pressure (front / rear, cold) | 33 psi / 33 psi (227 kPa) |
| Current tyres (brand, model) | — |
| Fitted at (odometer / date) | — |
| Spare type | — |
| Wheel nut torque | — |

## Fluids & consumables

| Item | Spec | Capacity | Interval |
|---|---|---|---|
| Engine oil | — | — | — |
| Oil filter | — | — | — |
| Air filter | — | — | — |
| Cabin filter | — | — | — |
| Coolant | — | — | — |
| Brake fluid | — | — | — |
| Transmission fluid | — | — | — |
| Spark plugs | — | — | — |
| Battery | — | — | — |
| Wiper blades | — | — | — |

## Key numbers & codes

| Field | Value |
|---|---|
| Key / remote type | — |
| Radio / nav code | — |
| Paint code | — |
| Service book / portal | — |
| Roadside assist member no. | — |

## Ownership

| Field | Value |
|---|---|
| Purchased (date) | — |
| Purchased from | — |
| Purchase price | — |
| Odometer at purchase | — |
| Finance / lease | — |
| Payout / end date | — |

## Insurance & registration

| Field | Value |
|---|---|
| Insurer | — |
| Policy number | — |
| Cover type | — |
| Excess | — |
| Agreed / market value | — |
| Premium | — |
| Policy renewal | — |
| Registration expiry | 2026-12-22 |
| Registration status | CURRENT (checked 2026-08-24) |
| Purpose of use | DEALER — see notes |
| CTP insurer | — |
| Roadside assist expiry | — |

## Notes

Odometer 190,000 km as at 2026-08-24 (see `data/odometer.csv`).

Registration details confirmed 2026-08-24 from a Queensland rego check.

**Purpose of use is recorded as DEALER.** If the car is privately owned and
driven, this is likely to need changing to a private purpose of use — it
affects the CTP class, the registration fee, and potentially whether an
insurance claim is honoured. Worth checking with TMR.

**VIN year code.** The 10th character of the VIN is `L`, which under the
usual convention indicates a 2020 model year, while the registration record
describes it as a 2019 HR-V. A build-date versus model-year difference is
common and usually harmless, but confirm against the compliance plate before
ordering year-specific parts.

Placard pressure is 33 psi cold, front and rear. `./car.py tyres` reads that
figure from this table as its default target, so update it here if the
placard says otherwise or a different tyre size is fitted.

Still to confirm: build date, engine and transmission, tyre size and
pressures from the placard, and service history to date.
