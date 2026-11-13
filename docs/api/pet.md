# API 계약 — 반려동물

공통 응답 형식은 [API 명세 안내](README.md)를 참고한다.

---

### 반려동물 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/pets` | 보호자 본인 | `없음` | `200 [{"petId":"pet-1","name":"루이","species":{"speciesId":1,"name":"강아지"},"breed":{"breedId":2,"name":"푸들"},"profileImageUrl":null,"ageYears":3,"sex":"MALE"}]` | 공통 인증·권한 오류 | No. 10, 25 · PET-01 |

본인 소유만 반환한다. 생년월일 미상인 경우 ageYears는 null이다. 상담 시 이 목록에서 한 마리를 선택한다.

### 반려동물 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/pets/{petId}` | 보호자 본인 | `petId` | `200 PetDetail` | 404 NOT_FOUND | No. 11 · PET-01 |

타임라인은 같은 petId의 건강 기록 목록에서 조회한다.

### 반려동물 등록

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/pets` | 보호자 본인 | `{"name":"루이","speciesId":1,"breedId":2,"birthDate":"2023-05-01","sex":"MALE","neutered":true,"weight":4.2,"basicVaccinated":null,"profileMediaId":null}` | `201 PetDetail` | 400 VALIDATION_ERROR, 404 NOT_FOUND | No. 12 · PET-01 · D12 |

name, speciesId, breedId, sex는 필수 초안이다. 나머지 필드는 선택·nullable 초안이다. 품종은 같은 종에 속해야 한다. 체중 단위·범위는 미정이다.

### 반려동물 정보 수정

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/pets/{petId}` | 보호자 본인 | `등록 필드 중 변경할 필드` | `200 PetDetail` | 400 VALIDATION_ERROR, 404 NOT_FOUND | No. 13 · PET-01 · D12 |

종과 품종의 조합을 최종 값 기준으로 검증한다. 프로필 체중과 체중 기록의 동기화 정책은 미정이다.

### 반려동물 삭제

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `DELETE` | `/api/pets/{petId}` | 보호자 본인 | `petId` | `204 본문 없음` | 404 NOT_FOUND, 409 PET_HAS_OPEN_CONSULTATION | No. 14 · PET-01 · D11 |

요구사항은 소프트 삭제다. 진행 중 상담과 기록의 조회·보존 기준은 미정이다.

### 종·품종 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/pet-species` | 보호자 | `없음` | `200 [{"speciesId":1,"name":"강아지","breeds":[{"breedId":2,"name":"푸들"}]}]` | 공통 인증·권한 오류 | No. 12, 13 · PET-01 |

등록·수정 화면에서 선택할 종·품종이다.

## 응답 필드와 데이터 정책

- `PetDetail` = 목록 항목 + `birthDate: date?`, `neutered: boolean?`, `weight: number?`, `basicVaccinated: boolean?`. `sex`는 `MALE`, `FEMALE` 초안이다.
- `petId`는 문자열, `speciesId`와 `breedId`는 정수다. `profileMediaId`는 문자열이며 응답은 접근 검사를 거치는 `profileImageUrl`을 반환한다.
