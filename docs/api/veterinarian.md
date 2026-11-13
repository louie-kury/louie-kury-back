# API 계약 — 수의사·병원 탐색

공통 응답 형식은 [API 명세 안내](README.md)를 참고한다.

---

### 수의사 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/veterinarians` | 보호자 | `page, size` | `200 Page<VeterinarianSummary>` | 400 VALIDATION_ERROR | No. 23 · VET-01 · D16 |

병원에 소속되고 심사를 통과한 수의사 중 신규 상담을 받을 수 있는 수의사만 반환한다. 검색·정렬·페이지 조회 방식은 미정이다.

### 수의사 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/veterinarians/{veterinarianId}` | 보호자 | `veterinarianId` | `200 VeterinarianDetail` | 404 NOT_FOUND | No. 24 · VET-01 · D16 |

프로필에 소속 병원, 선택 사진, 직책, 진료 동물·일정, 소개, 경력과 평가 요약을 제공한다. 프로필·일정·병원 상세 필드 일부는 ERD 저장 구조가 미정이다.

### 수의사 공개 후기 목록

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/veterinarians/{veterinarianId}/reviews` | 보호자 | `veterinarianId, page, size` | `200 Page<VeterinarianReview>` | 400 VALIDATION_ERROR, 404 NOT_FOUND | PRD REV-01 · VET-01 · D16 |

공개 대상 후기만 반환한다. 평가 수가 0이면 평균 평점은 null이다. 리뷰 표시명과 숨김 후 집계는 미정이다.

### 지도 병원 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/hospitals` | 보호자 | `region, latitude·longitude(쌍), specialty, page, size` | `200 Page<Hospital>` | 400 VALIDATION_ERROR | No. 2 · 지도 |

지역·현재 위치·진료 분야 필터를 제공한다. 좌표 저장, 검색 반경과 정렬 기준, 비로그인 공개 여부는 미정이다.

### 지도 병원 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/hospitals/{hospitalId}` | 보호자 | `hospitalId` | `200 Hospital` | 404 NOT_FOUND | No. 2, 24 · VET-01 |

등록되어 공개 가능한 병원을 반환한다. 지도와 수의사 프로필은 같은 병원 식별자를 사용한다.

## 응답 필드와 데이터 정책

| 응답 타입 | 필드 |
|---|---|
| VeterinarianSummary | `veterinarianId: string`, `name: string`, `profileImageUrl: string?`, `hospital: {hospitalId,name}` |
| VeterinarianDetail | VeterinarianSummary의 `hospital`을 Hospital로 확장 + `position: string?`, `treatedSpecies: string[]`, `schedule: ScheduleSlot[]`, `introduction: string?`, `career: string[]`, `averageRating: number?`, `reviewCount: integer` |
| ScheduleSlot | `dayOfWeek: string`, `opensAt: HH:mm`, `closesAt: HH:mm`. 요일 코드 및 휴진·예약 가능 시간 표시 방식은 미정 |
| VeterinarianReview | `displayName: string`, `rating: number`, `content: string?`, `createdAt: datetime` |
| Hospital | `hospitalId: string`, `name: string`, `address: string`, `detailAddress: string?`, `phoneNumber: string`, `location: {latitude,longitude}?`(두 값 모두 number), `openingHours: ScheduleSlot[]`, `treatedSpecies: string[]`, `specialties: string[]` |
