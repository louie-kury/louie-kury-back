# API 계약 — 건강 기록

공통 응답 형식은 [API 명세 안내](README.md)를 참고한다.

---

### 건강 기록 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/pets/{petId}/health-records` | 보호자 본인 | `date(YYYY-MM-DD, 선택), type(선택), page, size` | `200 Page<HealthRecordSummary>` | 400 VALIDATION_ERROR, 404 NOT_FOUND | No. 18 · HLT-02 · D12 |

같은 날짜와 반려동물로 조회한 달력과 목록은 동일한 기록을 반영한다.

### 건강 기록 달력 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/pets/{petId}/health-records/calendar` | 보호자 본인 | `month(YYYY-MM, 필수)` | `200 {"dates":["2026-11-10","2026-11-12"]}` | 400 VALIDATION_ERROR, 404 NOT_FOUND | No. 18 · HLT-02 · D12 |

기록이 있는 날짜만 오름차순으로 반환한다. 빈 달은 dates가 빈 배열이다.

### 건강 기록 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/pets/{petId}/health-records/{recordId}` | 보호자 본인 | `petId, recordId` | `200 HealthRecord` | 404 NOT_FOUND | No. 19 · HLT-01·02 · D12 |

기록이 지정한 반려동물에 속해야 한다.

### 건강 기록 등록

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/pets/{petId}/health-records` | 보호자 본인 | `{"type":"WOUND","observedAt":"2026-11-12T09:00:00+09:00","details":[{"subType":null,"textValue":"왼쪽 앞발 상처","numericValue":null}],"mediaIds":[]}` | `201 HealthRecord` | 400 VALIDATION_ERROR, 404 NOT_FOUND | No. 20 · HLT-01·04 · D12 |

type, observedAt는 필수 초안이다. 유형별 입력값과 첨부 제한은 미정이다. 본인 업로드만 연결할 수 있다.

### 건강 기록 수정

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/pets/{petId}/health-records/{recordId}` | 보호자 본인 | `등록 필드 중 변경할 필드` | `200 HealthRecord` | 400 VALIDATION_ERROR, 404 NOT_FOUND | No. 21 · HLT-01·04 · D12 |

수정 허용 범위와 수의사 공유 반영 방식(D05)은 미정이다.

### 건강 기록 삭제

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `DELETE` | `/api/pets/{petId}/health-records/{recordId}` | 보호자 본인 | `petId, recordId` | `204 본문 없음` | 404 NOT_FOUND | No. 22 · HLT-01·04 · D05·D12 |

요구사항은 소프트 삭제다. ERD에는 건강기록 삭제 표식이 없으며 삭제 및 첨부 보관 규칙은 미정이다.

### 예방접종 이력 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/pets/{petId}/vaccinations` | 보호자 본인 | `page, size` | `200 Page<Vaccination>` | 400 VALIDATION_ERROR, 404 NOT_FOUND | PRD HLT-03 · D12 |

기본 예방접종 여부는 반려동물 프로필의 별도 항목이다.

### 예방접종 이력 등록

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/pets/{petId}/vaccinations` | 보호자 본인 | `{"vaccineNameId":"vac-1","vaccinatedAt":"2026-11-12T09:00:00+09:00"}` | `201 Vaccination` | 400 VALIDATION_ERROR, 404 NOT_FOUND | PRD HLT-03 · D12 |

접종명 참조 키의 ERD 타입이 서로 다르다. 필수 항목, 접종명 선택지 공급, 수정·삭제 범위는 미정이다.

### 병원 진료 이력 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/pets/{petId}/clinic-visits` | 보호자 본인 | `page, size` | `200 Page<ClinicVisit>` | 400 VALIDATION_ERROR, 404 NOT_FOUND | PRD HLT-03 · D12 |

방문 시각을 기준으로 조회한다.

### 병원 진료 이력 등록

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/pets/{petId}/clinic-visits` | 보호자 본인 | `{"visitedAt":"2026-11-12T09:00:00+09:00","type":"외래","content":"정기 검진"}` | `201 ClinicVisit` | 400 VALIDATION_ERROR, 404 NOT_FOUND | PRD HLT-03 · D12 |

필수 항목과 진료 유형·수정·삭제 범위는 미정이다.

## 응답 필드와 데이터 정책

| 응답 타입 | 필드 |
|---|---|
| HealthRecordSummary | `recordId: integer`, `type: string`, `observedAt: datetime`, `summary: string?` |
| HealthRecord | HealthRecordSummary + `petId: string`, `details: Detail[]`, `media: MediaRef[]`, `createdAt: datetime`, `updatedAt: datetime` |
| Detail | `subType: string?`, `textValue: string?`, `numericValue: number?` |
| Vaccination | `vaccinationId: string`, `vaccineNameId: string`, `vaccineName: string`, `vaccinatedAt: datetime` |
| ClinicVisit | `visitId: string`, `visitedAt: datetime`, `type: string`, `content: string` |

유형 초안은 `STOOL`(변 상태), `WOUND`, `MEDICATION`, `FOOD`, `WATER`, `VOMIT`, `ACTIVITY_CHANGE`, `WEIGHT`, `OTHER`다. 복용약에는 복용 시각이 필요하다. 복용약·활동 변화·기타는 요구사항 시트에 있으며 PRD·ERD 기존 유형에 추가 합의가 필요하다. 복용 시각이 관찰 시각과 다른 경우의 입력 구조 및 상세 유형별 단위는 D12에서 정한다.
