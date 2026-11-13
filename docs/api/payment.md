# API 계약 — 결제·코인·정산

공통 응답 형식은 [API 명세 안내](README.md)를 참고한다.

---

### 내 코인 지갑 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/wallets/me` | 보호자 본인 | `없음` | `200 {"balanceCoins":10000}` | 공통 인증·권한 오류 | PRD PAY-01·02 |

잔액은 코인 정수이며 지정 예약 신청과 즉시 상담 매칭 확정 시 각각 7,000코인 차감을 반영한다. 즉시 상담 미매칭·매칭 전 취소에는 변동이 없다.

### 코인 원장 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/wallets/me/transactions` | 보호자 본인 | `type(선택), page, size` | `200 Page<CoinTransaction>` | 400 VALIDATION_ERROR | PRD PAY-01·02·03 |

충전·사용·반환·현금 환불 회수 내역을 원거래와 연결한다.

### 코인 충전 상품 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/coin-products` | 보호자 | `없음` | `200 [{"productCode":"COIN_7000","coins":7000,"amountKrw":7700}]` | 공통 인증·권한 오류 | PRD PAY-01 · D01 |

7,000코인 상품의 결제액은 7,700원이다. 공급가액은 7,000원이고 부가세는 700원이다. 결제 성공 확인 후 7,000코인을 한 번 지급한다. 그 외 상품·환산·한도·유효 기간은 미정이다.

### 코인 충전 주문 생성

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/coin-charge-orders` | 보호자 본인 | `Idempotency-Key 필수. {"productCode":"COIN_7000"}` | `201 ChargeOrder` | 400 VALIDATION_ERROR, 409 IDEMPOTENCY_CONFLICT, 503 PROVIDER_UNAVAILABLE | PRD PAY-01 · D01 |

금액과 지급 코인을 서버가 상품에서 결정한다. 결제창 연결 정보와 만료 방식은 제공사 확정 후 명세한다.

### 코인 충전 주문 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/coin-charge-orders/{orderId}` | 주문 보호자 | `orderId` | `200 ChargeOrder` | 404 NOT_FOUND | PRD PAY-01 · D01 |

결제 승인과 코인 지급 상태를 구분한다. 외부 승인 후 지급 실패는 복구 대상으로 남긴다.

### 코인 충전 현금 환불 신청

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/coin-charge-orders/{orderId}/refunds` | 주문 보호자 | `Idempotency-Key 필수. {"reason":"미사용 충전 취소"}` | `202 {"refundId":"refund-1","status":"REQUESTED"}` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 REFUND_NOT_ELIGIBLE / IDEMPOTENCY_CONFLICT | PRD PAY-03 · D10 |

기획상 미사용 충전이 신청 대상이다. 일부 사용 제한, 사용액 배정, 반환 후 자격 및 법적 예외는 미정이다. 외부 환불과 내부 코인 회수의 정합성을 보장한다.

### 현금 환불 진행 상태 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/coin-charge-orders/{orderId}/refunds/{refundId}` | 주문 보호자 | `orderId, refundId` | `200 {"refundId":"refund-1","orderId":"order-1","status":"REQUESTED","amountKrw":null,"recoveredCoins":null}` | 404 NOT_FOUND | PRD PAY-03 · D10 |

환불 성공 확인과 코인 회수가 반영되어야 완료로 표시한다. 환불액·회수 코인·세부 상태는 D10에서 확정한다.

### 내 수의사 정산 목록

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/veterinarians/me/settlements` | 수의사 본인 | `month, status, page, size` | `200 Page<Settlement>` | 400 VALIDATION_ERROR | PRD SET-01 · D02 |

지정 예약과 즉시 상담 모두 완료된 유료 상담을 한 번씩 집계한다. 건당 부가세 700원을 제외한 7,000원에 플랫폼 수수료 20%(1,400원)를 적용하고 수의사 배분액 5,600원을 매월 25일 정산 후 가입 시 등록한 소속 병원 명의 사업자 계좌로 자동 이체 요청한다. 이체 성공 확인 후 지급 완료로 표시하고 실패를 기록한다. 마감·휴일·계좌 변경 시 기존 상담의 지급 계좌·지급 재시도는 D02에서 확정한다.

## 응답 필드와 데이터 정책

| 응답 타입 | 필드 |
|---|---|
| CoinTransaction | `transactionId: string`, `type: string`, `coinDelta: integer`, `balanceAfter: integer`, `relatedType: string`, `relatedId: string`, `createdAt: datetime` |
| ChargeOrder | `orderId: string`, `productCode: string`, `coins: integer`, `amountKrw: integer`, `paymentStatus: string`, `creditStatus: string`, `expiresAt: datetime?` |
| Settlement | `settlementId: string`, `veterinarianId: string`, `consultationId: string`, `coins: integer`, `basisAmountKrw: integer`, `commissionRate: number`, `commissionAmountKrw: integer`, `payoutAmountKrw: integer`, `payoutAccountId: string?`, `status: string`, `paidAt: datetime?` |

API `commissionRate`는 비율이므로 `0.20`이 20%를 뜻한다. ERD에는 퍼센트 단위로 기록한다. `payoutAccountId`는 병원 정산 계좌의 불투명 식별자다. 이체 요청 시 대상 계좌가 확정되어야 하며 응답에는 계좌번호를 포함하지 않는다. 결제창 성공 표시만으로 코인을 지급하지 않는다. 제공사 결제 승인·취소 통지 및 검증 계약은 D01·D10, 자동 지급 통지 계약은 D02 확정 이후 정의한다. 서명 검증, 재전송 중복 방지, 금액 대사 및 승인 후 지급 실패 복구가 필요하다.
