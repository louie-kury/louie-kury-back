# API 계약 — 상담·일지·후기

공통 응답 형식은 [API 명세 안내](README.md)를 참고한다.

---

### 지정 수의사 예약 요청

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations` | 보호자 | `Idempotency-Key 필수. {"petId":"pet-1","veterinarianId":"vet-1","channel":"CHAT","preferredAt":"2026-11-15T14:00:00+09:00","content":"며칠 전부터 구토가 있어요."}` | `201 Consultation (REQUESTED). 동일 요청 재시도 시 최초 결과 반환` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 INSUFFICIENT_COINS / VETERINARIAN_UNAVAILABLE / IDEMPOTENCY_CONFLICT | No. 25~27 · CON-01·03 · PAY-02 · D03 |

내용은 자유 양식 1,000자 이내다. 본인 반려동물 한 마리, 수의사, 희망 일시와 수단 하나를 지정한다. 서버가 예약 생성과 7,000코인 차감을 한 번에 처리한다. ERD의 필수 상담 제목은 입력 요구사항에 없어 저장 기준 확인이 필요하다.


### 위치 기반 즉시 상담 신청

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/instant` | 보호자 | `Idempotency-Key 필수. {"petId":"pet-1","channel":"VIDEO","location":{"latitude":37.5,"longitude":127.0},"content":"구토가 있어요."}` | `201 Consultation (MATCHING). matchExpiresAt 포함, veterinarian은 null` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 IDEMPOTENCY_CONFLICT | PRD CON-03·05 · PAY-02 · D05·D15·D17 |

`petId`는 보호자 본인 반려동물, `channel`은 세 수단 중 하나다. `location` 좌표 입력과 `content`(선택)는 계약 초안이다. 위치 확인·권한 거부 대응은 D17에서 확정한다. 서버가 요청 접수 시각부터 60초 기한을 계산한다. 신청과 탐색에는 코인을 차감하지 않는다. 미매칭 안내창을 닫을 때 서버 상태는 그대로이며 다시 신청하면 새 멱등 키로 새 매칭을 시작한다.

### 즉시 상담 대기 시작

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/instant/wait-sessions` | 상담 제공이 가능한 수의사 | `본문 없음` | `201 {"waitSessionId":"wait-1"}` | 409 VETERINARIAN_BUSY | PRD CON-05 · D15·D17 |

대기 화면을 띄운 상태에서 시작하는 세션 초안이다. 서버는 현재 대기 중인 수의사에게만 새 요청을 전달한다. 다른 탭을 보거나 화면이 잠겨 있으면 대기에서 제외한다. 세션의 연결 유지·만료·화면 활성 상태 확인 방식은 D15·D17에서 확정한다.

### 즉시 상담 대기 목록 구독

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/consultations/instant/wait-sessions/{waitSessionId}/requests` | 본인 대기 세션의 수의사 | `waitSessionId` | `200 실시간 목록 스트림. 초기 스냅샷과 추가·제거 갱신에 InstantOffer 사용` | 404 NOT_FOUND | PRD CON-05 · D05·D15·D17 |

초기 목록과 실시간 갱신에는 수락 가능한 요청만 포함한다. 한 요청이 여러 단계에 걸쳐도 같은 수의사 목록에는 한 건만 유지한다. 매칭·미매칭·매칭 전 취소 시 즉시 제거하며 경쟁 수락자에게 매칭 결과를 알린다. 전송 프로토콜, 이벤트 형식·재동기화·정렬은 D15에서 확정한다.

### 즉시 상담 대기 종료

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `DELETE` | `/api/consultations/instant/wait-sessions/{waitSessionId}` | 본인 대기 세션의 수의사 | `waitSessionId` | `204 본문 없음` | 404 NOT_FOUND | PRD CON-05 · D15·D17 |

대기 화면을 벗어난 세션은 새 요청 전달 대상에서 제외한다. 화면을 벗어나기 전 이미 받은 요청의 수락 조건은 D17에서 확정한다.

### 즉시 상담 수락

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/{consultationId}/accept` | 상담 제공이 가능하고 해당 요청을 전달받은 수의사 | `Idempotency-Key 필수. 본문 없음` | `200 Consultation (MATCHED)` | 404 NOT_FOUND, 409 MATCH_ALREADY_RESOLVED / VETERINARIAN_BUSY / INSUFFICIENT_COINS / IDEMPOTENCY_CONFLICT | PRD CON-05 · PAY-02 · D15·D17 |

지정 예약 또는 즉시 상담을 진행 중인 수의사는 수락할 수 없다. 기한과 요청 상태를 서버에서 확인하고 담당 수의사 확정과 7,000코인 차감을 한 번에 처리한다. 최초 유효 수락만 성립하며 나머지 수락에는 종료 결과를 반환한다. 잔액 부족 시 매칭을 확정하지 않고 보호자에게 `코인이 부족해 상담을 연결할 수 없어요.`를 표시한다. 잔액 부족 이후 탐색·요청의 처리와 보호자 전달 채널은 D15·D17에서 확정한다. 매칭된 두 당사자는 신청 시 선택한 수단의 연결 흐름으로 이어진다. 매칭 결과만으로 연결 성공을 표시하지 않는다. 수락 후에도 기존 건강 기록이나 요약에 대한 접근 권한은 생기지 않는다.

#### 즉시 상담 탐색 일정

| 접수 후 경과 | 탐색 반경 |
| --- | --- |
| 0초 | 500m |
| 10초 | 1km |
| 20초 | 1.5km |
| 30초 | 5km |
| 40초부터 60초 직전까지 | 10km |

각 단계에서 보호자 위치를 기준으로 대상 병원을 찾고, 해당 병원에 소속된 대기 수의사에게 동시에 전달한다. 새로 대상에 포함된 수의사에게만 추가 전송한다. 매칭 확정 시 즉시 탐색을 끝낸다. 기한까지 미매칭이면 코인 변동 없이 `UNMATCHED`로 종료한다. 보호자 상세 조회에서 종료 상태를 확인할 수 있으며 보호자에게 `지금 바로 상담할 수 있는 수의사를 찾지 못했어요.`를 표시한다. 보호자에게 결과를 실시간 전달하는 채널은 D15에서 확정한다.

### 내 상담 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/consultations` | 보호자·수의사 | `requestType(선택), status(선택), page, size` | `200 Page<ConsultationSummary>` | 400 VALIDATION_ERROR | No. 40, 42 · CON-01·04 |

보호자는 자신이 요청한 건, 수의사는 담당 건을 조회한다. 수의사의 지정 예약 신규 탭은 `RESERVATION`과 `REQUESTED`, 완료 탭은 `COMPLETED`로 조회한다. 수락 전 즉시 상담 요청은 전용 대기 목록에서 조회한다.

### 내 상담 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/consultations/{consultationId}` | 상담 당사자 | `consultationId` | `200 Consultation` | 404 NOT_FOUND | No. 41, 43 · CON-01·04 · D05 |

반려동물 이름·종·품종과 보호자가 작성한 상담 내용을 반환한다. 지정 예약 요청 단계의 건강 요약 필드는 D05에서 확정한다. 즉시 상담은 매칭 전 보호자만 이 상세를 조회할 수 있으며, 매칭 후에도 담당 수의사에게 기존 건강 기록과 건강 요약을 제공하지 않는다.

### 예약 승인

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/{consultationId}/approve` | 승인된 담당 수의사 | `consultationId, 본문 없음` | `200 Consultation (APPROVED)` | 404 NOT_FOUND, 409 INVALID_CONSULTATION_STATE | PRD CON-02 · D03·D05 |

지정 예약 요청 상태에서 승인한다. 코인 차감 상태를 유지하고 해당 상담에 따른 건강 기록 열람 권한을 부여한다.

### 예약 거절

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/{consultationId}/reject` | 승인된 담당 수의사 | `consultationId, 본문 없음` | `200 Consultation (REJECTED)` | 404 NOT_FOUND, 409 INVALID_CONSULTATION_STATE | PRD CON-02 · PAY-02 · D04·D05·D06 |

지정 예약 요청 상태에서 거절한다. 해당 예약에서 차감한 코인을 한 번만 전액 반환한다. 이후 기록과 연결 권한은 미정이다.

### 상담 취소

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/{consultationId}/cancel` | 매칭 전 즉시 상담은 요청 보호자. 그 외 주체 미정 | `consultationId, 본문 없음` | `200 Consultation (CANCELLED)` | 403 FORBIDDEN, 404 NOT_FOUND, 409 INVALID_CONSULTATION_STATE | PRD CON-04·05 · PAY-02 · D04·D05·D06·D17 |

즉시 상담 매칭 전 취소는 잔액을 유지하고 대기 목록에서 즉시 제거한다. 지정 예약 및 즉시 상담 매칭 후 취소가 성립하면 실제 차감 코인을 한 번 전액 반환한다. 승인·수락과 취소가 경합해도 상담 상태와 원장 결과가 일치해야 한다. 취소 주체·기한·매칭 이후 허용 조건과 후속 권한은 D04·D05·D06·D17에서 확정한다.

### 상담 연결 요청

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/{consultationId}/connections` | 상담 당사자. 안심번호 발신은 담당 수의사 | `Idempotency-Key 필수. consultationId, 본문 없음` | `202 ConsultationConnection` | 403 FORBIDDEN, 404 NOT_FOUND, 409 INVALID_CONSULTATION_STATE / IDEMPOTENCY_CONFLICT, 503 PROVIDER_UNAVAILABLE | No. 27 · CON-03·05 · D06 |

승인된 지정 예약 또는 매칭된 즉시 상담에서 서버가 신청 시 선택한 수단으로 연결한다. 제3자 참여를 차단한다. 안심번호는 담당 수의사가 보호자에게 발신하며 양쪽 실제 번호를 공개하지 않는다. 전화 통화 시간에 따른 추가 차감과 고정 자동 종료는 없다. 채팅·화상 참여 정보, 제공 업체, 수단 변경 및 재연결 허용 상태는 D06에서 확정한다. 새 연결 시도는 새 멱등 키를 사용한다.

### 상담 연결 상태 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/consultations/{consultationId}/connections/{connectionId}` | 상담 당사자 | `consultationId, connectionId` | `200 ConsultationConnection` | 404 NOT_FOUND | PRD CON-03 · D06 |

연결 상태가 `FAILED`이거나 연결 요청 자체가 제공사 장애로 실패하면 상담은 완료 처리하지 않는다. 보호자에게 `수의사와 연결하지 못했어요. 다시 연결해 주세요.`를 표시하고 재연결 절차를 제공한다. 재연결 이후 취소가 성립하면 실제 차감 코인을 전액 반환한다.

### 상담 완료

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/{consultationId}/complete` | 승인된 담당 수의사 | `consultationId, 본문 없음` | `200 Consultation (COMPLETED)` | 404 NOT_FOUND, 409 INVALID_CONSULTATION_STATE | PRD CON-04 · SET-01 · D03·D04·D05 |

확인창 ‘상담을 무사히 마쳤나요?’에서 담당 수의사가 ‘완료’를 선택할 때 호출한다. 창을 열 때는 상태가 바뀌지 않는다. 두 신청 유형 모두 사용을 확정하고 정산에 한 번만 반영한다. 완료 즉시 해당 상담의 건강 기록 권한을 종료하고 일지 작성 화면으로 이동한다. 같은 완료 재시도는 기존 결과를 반환한다.

### 보호자 신고로 상담 완료

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/{consultationId}/complete-with-report` | 상담을 담당한 수의사 | `Idempotency-Key 필수. 신고 사유·입력 필드는 D04 미정` | `200 {"consultationId":"con-1","status":"COMPLETED","reportId":"report-1"}` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 INVALID_CONSULTATION_STATE / IDEMPOTENCY_CONFLICT | PRD CON-04 · COM-02 · SET-01 · D04·D05 |

완료 확인창의 ‘보호자 신고’ 선택 후 제출할 때 호출한다. 신고 대상과 신고자는 서버가 해당 상담의 보호자와 담당 수의사로 결정하고 상담과 연결한다. 신고 접수와 상담 완료는 한 번에 반영한다. 접수가 실패하면 상담 완료·정산 확정도 발생하지 않는다. 일반 완료와 경합해도 코인 사용 확정·정산은 한 번만 성립한다. 성공하면 일지 작성 화면으로 이동한다. 신고 사유·입력값·실패 화면은 D04에서 확정한다.


### 상담 중 반려동물 건강 기록 목록

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/consultations/{consultationId}/health-records` | 승인된 지정 예약의 담당 수의사 | `date, type, page, size` | `200 Page<HealthRecordSummary>` | 400 VALIDATION_ERROR, 403 HEALTH_ACCESS_DENIED, 404 NOT_FOUND | PRD CON-02·04 · HLT-02 · D05 |

상담에 연결된 반려동물로 조회 범위를 결정한다. 즉시 상담은 매칭 후에도 이 경로와 파일 경로의 건강 기록 열람 권한을 부여하지 않는다. 완료된 해당 상담으로는 열람 권한을 얻을 수 없다. 접종·진료·미디어·복수 승인 예약은 D05에서 확정한다.

### 상담 중 반려동물 건강 기록 상세

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/consultations/{consultationId}/health-records/{recordId}` | 승인된 지정 예약의 담당 수의사 | `consultationId, recordId` | `200 HealthRecord` | 403 HEALTH_ACCESS_DENIED, 404 NOT_FOUND | PRD CON-02·04 · HLT-01·04 · D05 |

기록이 상담에 연결된 반려동물의 기록인지 검증한다. 응답의 첨부 범위는 D05에서 확정한다.

### 상담 일지 작성

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/{consultationId}/journal` | 완료한 담당 수의사 | `{"content":"보호자가 설명한 상태와 상담 내용을 기록했습니다."}` | `201 Journal` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 INVALID_CONSULTATION_STATE / JOURNAL_ALREADY_EXISTS | No. 44 · LOG-01 · D07 |

완료된 담당 상담에만 작성한다. ERD의 상담당 일지 필드 1개를 반영한 초안이다. 공개 절차와 작성 기한은 미정이다.

### 상담 일지 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/consultations/{consultationId}/journal` | 해당 보호자·담당 수의사 | `consultationId` | `200 Journal` | 404 NOT_FOUND | PRD LOG-01 · D05·D07 |

보호자는 공개된 일지를 조회한다. 일지 조회 권한은 비공개 건강 기록이나 첨부의 권한을 부여하지 않는다.

### 상담 일지 수정

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/consultations/{consultationId}/journal` | 작성한 담당 수의사 | `{"content":"상담 내용을 보완했습니다."}` | `200 Journal (updatedAt 포함)` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 JOURNAL_NOT_EDITABLE | No. 45 · LOG-01 · D07 |

요구사항의 마지막 수정 시각을 반환한다. 수정 권한·기한 및 ERD 저장 필드는 미정이다.

### 상담 후기 작성

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/consultations/{consultationId}/reviews` | 완료된 상담의 보호자 | `Idempotency-Key 필수. {"rating":5,"content":null}` | `201 {"consultationId":"con-1","rating":5,"content":null,"createdAt":"2026-11-15T15:00:00+09:00"}` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 INVALID_CONSULTATION_STATE / IDEMPOTENCY_CONFLICT | PRD REV-01 · D16 |

별점 필수, 텍스트 선택이다. 별점 범위와 상담당 허용 수·공개 정책은 미정이다. 5는 형식 예시이며 범위를 정하지 않는다.

## 응답 필드와 데이터 정책

| 응답 타입 | 필드 |
|---|---|
| ConsultationSummary | `consultationId: string`, `requestType: string`, `channel: string`, `feeCoins: integer`, `status: string`, `pet: {petId,name,speciesName,breedName}`, `veterinarian: {veterinarianId,name}?`, `preferredAt: datetime?`, `createdAt: datetime`, `matchedAt: datetime?`, `matchExpiresAt: datetime?` |
| Consultation | ConsultationSummary + `content: string?`, `completedAt: datetime?`, `cancelledAt: datetime?` |
| InstantOffer | `consultationId: string`(수락 식별자), `channel: string`, `species: string`(강아지·고양이), `matchExpiresAt: datetime`(60초 기준 남은 시간 계산용). 거리·보호자 정보·건강 정보는 제외한다. |
| ConsultationConnection | `connectionId: string`, `channel: string`, `status: string`(`PENDING`, `CONNECTED`, `FAILED` 초안), `createdAt: datetime`. 외부 연결 식별자와 실제 번호는 서버 내부에 둔다. |
| Journal | `consultationId: string`, `content: string`, `updatedAt: datetime?` |

`requestType`은 `RESERVATION`·`INSTANT`, `channel`은 `CHAT`·`VIDEO`·`MASKED_CALL` 초안이다. `feeCoins`는 신청에 적용한 요금 7,000코인이며 실제 차감 시점은 유형에 따라 다르다. `preferredAt`은 지정 예약에 필수다. `matchedAt`은 즉시 상담이 매칭될 때, `matchExpiresAt`은 즉시 상담에만 설정한다. 즉시 상담은 매칭 전 `veterinarian`이 null이다. API 상태는 지정 예약의 `REQUESTED`·`APPROVED`·`REJECTED`, 즉시 상담의 `MATCHING`·`MATCHED`·`UNMATCHED`, 공통 `CANCELLED`·`COMPLETED`를 사용하는 초안이다. 내부 상태와 전이 세부 조건은 D03·D04·D17에서 확정한다. 요약 및 상세는 양측 실제 번호를 포함하지 않는다. `completedAt` 및 일지 수정 시각의 저장 위치는 확인 대상이다. 건강 기록 응답 타입은 [건강 기록](health.md)을 따른다.
