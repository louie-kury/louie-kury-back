# API 계약 — 계정·인증

공통 응답 형식은 [API 명세 안내](README.md)를 참고한다.

---

### 일반 로그인

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/auth/login` | 공개 | `{"loginId":"loui-care","password":"Example!123"}` | `200 {"accessToken":"<token>","role":"CAREGIVER"}` | 400 VALIDATION_ERROR, 401 INVALID_CREDENTIALS, 403 ACCOUNT_UNAVAILABLE | No. 4, 31, 59 · ACC-01 · D11 |

관리자·수의사도 동일한 로그인 요청을 사용한다. 실제 권한은 서버가 계정에서 결정한다. 승인 대기 수의사의 로그인 및 접근 범위, 토큰 발급·만료·갱신 정책은 미정이다.

### 보호자 일반 가입

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/auth/caregivers` | 공개 | `{"name":"김보호","phoneNumber":"01000000000","nickname":"루이집사","loginId":"loui-care","password":"Example!123","email":"loui@example.com"}` | `201 {"caregiverId":"cg-1"}` | 400 VALIDATION_ERROR, 409 ACCOUNT_CONFLICT | No. 8 · ACC-01 · D11 |

요구사항의 입력 초안은 비밀번호 8~20자(영문·숫자·특수문자), 닉네임 최대 30자다. 조합 검증, 연락처 확인, 약관 동의와 유일성 정책은 D11에서 확정한다.

### 수의사 가입 및 면허 제출

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/auth/veterinarians` | 공개 | `multipart/form-data. JSON 파트 profile {name,phoneNumber,loginId,password,email,hospitalRegistration,payoutAccount}, 파일 파트 license(필수)` | `201 {"veterinarianId":"vet-1","verificationStatus":"PENDING"}` | 400 VALIDATION_ERROR, 409 ACCOUNT_CONFLICT, 413 FILE_TOO_LARGE, 415 UNSUPPORTED_MEDIA_TYPE | No. 34~36 · ACC-02 · D02·D11 |

동물병원에 소속된 수의사만 가입할 수 있다. 병원 정보, 해당 병원 명의 사업자 계좌와 면허를 필수로 제출한다. 누락 시 신청을 완료할 수 없다. 재직증명서와 통장 사본은 수집하지 않는다. 사업자등록증 제출 여부, 소속 확인 방식 및 면허 파일 제한은 D11에서 확정한다. 계좌 원문과 면허는 공개 응답에서 제외한다.

### 소셜 로그인 시작

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/auth/oauth/{provider}/authorize` | 공개 | `provider: kakao, naver, google` | `302 Location 헤더로 제공자 인증 화면 이동` | 400 VALIDATION_ERROR, 503 PROVIDER_UNAVAILABLE | No. 5, 9 · ACC-01 · D11 |

제공 여부와 계정 연결 정책은 미정이다. 승인된 리다이렉트만 사용하고 요청과 콜백을 state로 연결한다.

### 소셜 로그인 콜백

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/auth/oauth/{provider}/callback` | 공개 · OAuth 검증 | `쿼리 code, state 또는 제공자 실패 응답` | `302 Location 헤더로 로그인 결과 또는 추가 가입 화면 이동` | 400 OAUTH_CALLBACK_INVALID, 503 PROVIDER_UNAVAILABLE | No. 5, 9 · ACC-01 · D11 |

추가 가입 여부를 구분하고 토큰을 URL에 포함하지 않는다. 프런트 세션 전달 방식은 미정이다.

### 소셜 가입 완료

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/auth/oauth/registrations` | 가입용 인증 증표 | `{"name":"김보호","phoneNumber":"01000000000"}` | `201 {"caregiverId":"cg-1","nickname":"루이친구42"}` | 400 VALIDATION_ERROR, 401 INVALID_REGISTRATION_PROOF, 409 ACCOUNT_CONFLICT | No. 9 · ACC-01 · D11 |

닉네임은 요구사항에 따라 서버가 생성한다. 가입 증표 전달 방식과 유효 기간은 미정이다.

### 아이디 찾기 요청

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/auth/login-id/recovery-requests` | 공개 | `{"name":"김보호","email":"loui@example.com"}` | `202 본문 없음` | 400 VALIDATION_ERROR, 429 RATE_LIMITED | No. 6, 32 · ACC-01 · D11 |

이름·이메일은 계정 검색에 사용한다. 일치 여부와 아이디의 전달 채널 및 본인 확인 절차는 미정이며 공개 응답에 계정 존재 여부를 드러내지 않는다.

### 비밀번호 재설정 요청

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/auth/password/reset-requests` | 공개 | `{"name":"김보호","loginId":"loui-care"}` | `202 본문 없음` | 400 VALIDATION_ERROR, 429 RATE_LIMITED | No. 7, 33, 60 · ACC-01 · D11 |

이름·아이디는 계정 식별에 사용한다. 재설정 증표 발급 전 소유 확인이 필요하며 확인 방법과 관리자 초기화 절차는 미정이다.

### 비밀번호 재설정

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/auth/password/resets` | 재설정 증표 | `{"resetToken":"<one-time-token>","newPassword":"Example!456"}` | `204 본문 없음` | 400 VALIDATION_ERROR, 401 INVALID_RESET_TOKEN | No. 7, 33, 60 · ACC-01 · D11 |

재설정 증표는 용도를 제한하고 한 번만 사용한다. 유효 기간과 변경 후 기존 세션 처리 기준은 미정이다.

### 내 회원 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/members/me` | 보호자·수의사 | `없음` | `200 보호자 {"nickname":"루이집사","email":"loui@example.com","phoneNumber":"01000000000","petCount":1} / 수의사 {"name":"김수의","email":"vet@example.com","phoneNumber":"01000000000","hospital":{"hospitalId":"hospital-1","name":"루이 동물병원"}}` | 공통 인증·권한 오류 | No. 15, 37 · ACC-01 |

수의사 `hospital`은 필수 소속 병원의 간략 정보(`hospitalId`, `name`)다.

### 내 회원 정보 수정

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/members/me` | 보호자·수의사 | `보호자 {nickname?,email?,phoneNumber?}, 수의사 {name?,email?,phoneNumber?}` | `200 내 회원 상세 조회와 같은 응답` | 400 VALIDATION_ERROR, 409 ACCOUNT_CONFLICT | No. 16, 38 · ACC-01 · D11·D16 |

연락처 변경 재확인은 미정이다. 수의사 이직·퇴직에 따른 소속 변경은 D11의 별도 심사 절차에서 정의한다. 비밀번호 변경은 전용 API를 사용한다.

### 내 비밀번호 변경

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PUT` | `/api/members/me/password` | 보호자·수의사 | `{"currentPassword":"Example!123","newPassword":"Example!456"}` | `204 본문 없음` | 400 VALIDATION_ERROR, 403 CURRENT_PASSWORD_INVALID, 409 PASSWORD_LOGIN_UNAVAILABLE | No. 16, 38 · ACC-01 · D11 |

소셜 전용 계정에 비밀번호를 설정할 수 있는지는 미정이다.

### 내 회원 탈퇴

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `DELETE` | `/api/members/me` | 보호자·수의사 | `없음` | `204 본문 없음` | 409 ACCOUNT_HAS_OPEN_OBLIGATIONS | No. 17, 39 · ACC-03 · D11 |

요구사항은 소프트 삭제다. 진행 중 상담, 충전 잔액, 정산, 재가입 및 보관·파기 규칙이 미정이며 응답 조건은 해당 정책과 함께 확정한다.

## 응답 필드와 데이터 정책

- `hospitalRegistration`은 필수 객체다. `name: string`, `businessRegistrationNumber: string`, `addressSelection: object`, `representativeName: string`을 받는다. `addressSelection`은 주소 검색 결과에서 선택한 병원 주소를 식별한다. 주소 검색 업체, 검증 가능한 선택값의 형식, 상세주소 입력 및 기존 병원 연결 기준은 D11에서 확정한다.
- `payoutAccount`는 필수 객체다. 해당 병원 명의의 사업자 계좌를 등록한다. 예금주 확인에는 금융결제원 오픈뱅킹 계좌실명조회 API를 사용한다. 은행·계좌 입력의 구체 필드, 서비스 이용 승인, 개인사업자·법인 계좌의 검증 범위와 조회 불가·명의 불일치 처리는 D02에서 확정한다. 계좌 정보는 ERD의 병원 정산 계좌와 연결한다.
- `role`은 `CAREGIVER`, `VETERINARIAN`, `ADMIN`이다. 계정 상태와 수의사 면허 심사 상태는 별개다.
- 비밀번호 입력은 인증·변경 요청으로만 받고 비밀번호와 해시를 API 응답에 포함하지 않는다.
