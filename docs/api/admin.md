# API 계약 — 관리자

공통 응답 형식은 [API 명세 안내](README.md)를 참고한다.

---

### 운영 대시보드 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/dashboard` | 관리자 · 대시보드 | `없음` | `200 {"caregiverCount":42,"veterinarianCount":7,"ongoingConsultationCount":3,"postCount":25,"hospitalCount":6,"receivedReportCount":2}` | 공통 인증·권한 오류 | No. 61 · ADM-01 |

각 집계의 탈퇴·숨김·처리 상태 포함 기준은 운영 정책에서 확정한다.

### 일반 회원 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/caregivers` | 관리자 · 회원관리 | `keyword(이름·이메일), status, page, size` | `200 AdminList<AdminMemberSummary> (총·활성·비활성 회원 수)` | 400 VALIDATION_ERROR | No. 62 · ADM-01 |

상태 필터 및 집계의 정지·탈퇴 매핑은 D11에서 확정한다.

### 일반 회원 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/caregivers/{caregiverId}` | 관리자 · 회원관리 | `caregiverId` | `200 AdminCaregiver` | 404 NOT_FOUND | No. 63 · ADM-01 · D11 |

계정 식별자·프로필·등록 반려동물 요약·신고 횟수를 반환한다. 비밀번호와 해시는 반환 필드에서 제외한다.

### 일반 회원 상태 변경

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/admin/caregivers/{caregiverId}/status` | 관리자 · 회원관리 | `{"status":"SUSPENDED","reason":"운영 정책 위반"}` | `200 AdminMemberSummary` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 INVALID_ACCOUNT_TRANSITION | No. 64 · ACC-03 · ADM-01 · D11 |

정지·해제·운영 탈퇴 처리의 세부 전이와 기존 거래 영향은 미정이다. 변경 사유, 처리자, 처리 시각을 감사 이력에 남긴다.

### 수의사 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/veterinarians` | 관리자 · 수의사관리 | `keyword(병원명·이름·이메일), status, verificationStatus, page, size` | `200 AdminList<AdminMemberSummary> (총·활성·비활성 수의사 수)` | 400 VALIDATION_ERROR | No. 65~66 · ACC-02 · ADM-01 |

verificationStatus로 심사 신청 목록을 조회한다. 계정 상태와 면허 심사 결과를 구분한다.

### 수의사 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/veterinarians/{veterinarianId}` | 관리자 · 수의사관리 | `veterinarianId` | `200 AdminVeterinarian` | 404 NOT_FOUND | No. 65, 67 · ACC-02 · ADM-01 · D11 |

심사자는 인가된 범위에서 면허, 병원명·사업자등록번호·주소·대표자명과 병원 계좌의 등록·명의 확인 결과를 조회한다. 비밀번호와 해시는 반환 필드에서 제외한다.

### 수의사 인증 심사

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/admin/veterinarians/{veterinarianId}/verification` | 관리자 · 수의사심사 | `{"decision":"APPROVE","reason":"면허 및 제출 자료 확인"} (APPROVE, REJECT)` | `200 {"veterinarianId":"vet-1","verificationStatus":"APPROVED","reviewedAt":"2026-11-12T11:30:00+09:00"}` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 INVALID_VERIFICATION_STATE | No. 65 · ACC-02 · ADM-01 · D11 |

면허, 소속 병원 정보 및 해당 병원 명의 사업자 계좌가 있는 가입 신청을 심사한다. 병원 미소속 수의사는 승인할 수 없다. 계좌 명의 불일치·조회 불가 처리 기준은 D02에서 확정한다. 처리자·시각·결과·사유를 기록한다. 심사 전이나 거절 후에는 상담 제공이 차단된다. 재심사·철회 정책과 심사 이력 저장은 미정이다.

### 수의사 계정 상태 변경

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/admin/veterinarians/{veterinarianId}/status` | 관리자 · 수의사관리 | `{"status":"SUSPENDED","reason":"운영 정책 위반"}` | `200 AdminMemberSummary` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 INVALID_ACCOUNT_TRANSITION | No. 68 · ACC-03 · ADM-01 · D11 |

처리자·시각·사유를 기록한다. 정지 상태에서는 신규 요청을 받지 못한다. 진행 중 상담·코인·정산 처리 절차는 미정이다.

### 신고 접수 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/reports` | 관리자 · 신고관리 | `targetType(필수), reasonCode, status, keyword, page, size` | `200 AdminList<ReportSummary> (총·처리·미처리 신고 수)` | 400 VALIDATION_ERROR | No. 69, 71, 73, 75 · COM-02 · ADM-01 · D08 |

targetType별 keyword 대상은 보호자 닉네임, 수의사 이름, 게시글 제목·작성자, 댓글 내용 일부·작성자다. 처리 상태와 신고 사유로 필터한다.

### 신고 접수 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/reports/{reportId}` | 관리자 · 신고관리 | `reportId` | `200 ReportDetail` | 404 NOT_FOUND | No. 70, 72, 74, 76 · COM-02 · ADM-01 · D08·D11 |

대상별 원문·작성자·신고자·사유·일시·관련 게시글·댓글·상담·증빙을 승인된 범위에서 제공한다. 상담 완료 시 접수된 보호자 신고는 `relatedConsultationId`와 담당 수의사 `reporter.userId`를 반환한다. 일반 신고의 증빙·관련 상담 연결 범위는 D08에서 확정한다.

### 신고 검토 및 처리

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/admin/reports/{reportId}/resolution` | 관리자 · 신고처리 | `{"status":"COMPLETED","action":"HIDE","reason":"운영 정책 위반 확인"}` | `200 ReportDetail` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 INVALID_REPORT_TRANSITION | No. 70, 72, 74, 76 · COM-02 · ADM-01 · D08 |

게시글·댓글의 조치 예시는 HIDE, KEEP, DELETE다. 대상별 조치·상태 전이는 미정이다. 결과·사유·처리자·일시를 기록하고 목록과 상세의 노출 정책을 함께 반영한다.

### 상담 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/consultations` | 관리자 · 상담관리 | `keyword(수의사·병원·반려동물), requestType, status, issue, page, size` | `200 AdminList<AdminConsultationSummary> (총·진행·지연·취소·미완료 건수)` | 400 VALIDATION_ERROR | No. 77 · ADM-01 · D03·D04 |

지정 예약과 즉시 상담을 유형별로 조회한다. 즉시 상담은 수의사 배정 전이거나 미매칭일 때 담당 수의사와 병원이 null이다. 지연과 미완료의 판정 기준은 미정이다. 요약 목록에는 상담 일지 본문을 포함하지 않는다.

### 상담 일지 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/consultations/{consultationId}/journal` | 관리자 · 일지열람 권한 미정 | `consultationId` | `200 {"consultationId":"con-1","caregiver":{"caregiverId":"cg-1","name":"김보호"},"pet":{"petId":"pet-1","name":"루이"},"journal":{"content":"상담 내용","updatedAt":null}}` | 403 FORBIDDEN, 404 NOT_FOUND | No. 78 · LOG-01 · ADM-01 · D05·D07 |

관리자의 열람 목적과 당사자 필드 범위가 미정이다. 예시 필드는 검토 대상이다.

### 상담 일지 삭제

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `DELETE` | `/api/admin/consultations/{consultationId}/journal` | 관리자 · 일지삭제 권한 미정 | `consultationId. 삭제 사유 전달 방식 미정` | `204 본문 없음` | 403 FORBIDDEN, 404 NOT_FOUND, 409 JOURNAL_NOT_DELETABLE | No. 79 · LOG-01 · ADM-01 · D07 |

요구사항은 소프트 삭제다. 삭제 사유 전달 방식, 권한, 보존 및 삭제 표식은 미정이다. 상담 완료와 정산 상태에는 영향을 주지 않는다.

### 상담 예외 취소

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/admin/consultations/{consultationId}/cancel` | 관리자 · 상담 예외처리 권한 미정 | `{"reason":"당사자 요청 접수"}` | `200 Consultation (CANCELLED)` | 400 VALIDATION_ERROR, 403 FORBIDDEN, 404 NOT_FOUND, 409 INVALID_CONSULTATION_STATE | PRD ADM-01 · CON-04·05 · PAY-02 · D04·D05·D06·D17 |

취소가 성립하면 실제 차감 코인을 한 번 전액 반환한다. 즉시 상담 매칭 전에는 잔액을 유지한다. 관리자 운영 예외 범위는 D04·D17에서 확정한다.

### 게시글 관리 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/community/posts` | 관리자 · 콘텐츠관리 | `keyword(제목·작성자), visibility, page, size` | `200 AdminList<AdminPostSummary> (전체·공개·비공개 건수)` | 400 VALIDATION_ERROR | No. 80 · ADM-01 · D08 |

숨김과 삭제 상태의 집계 기준은 미정이다.

### 게시글 관리 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/community/posts/{postId}` | 관리자 · 콘텐츠관리 | `postId` | `200 AdminPost` | 404 NOT_FOUND | No. 81 · ADM-01 · D08 |

게시글 원문·작성자·첨부·작성 및 수정 일시·노출 상태를 반환한다. 댓글 및 신고 이력은 아래 별도 API에서 페이지 조회한다.

### 게시글 관리 댓글 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/community/posts/{postId}/comments` | 관리자 · 콘텐츠관리 | `postId, page, size` | `200 Page<Comment>` | 400 VALIDATION_ERROR, 404 NOT_FOUND | No. 81 · ADM-01 · D08 |

삭제·숨김 원문 열람 범위는 운영 권한 정책에서 확정한다.

### 게시글 관리 신고 이력 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/community/posts/{postId}/reports` | 관리자 · 신고관리 | `postId, page, size` | `200 Page<ReportSummary>` | 400 VALIDATION_ERROR, 404 NOT_FOUND | No. 81 · ADM-01 · D08 |

해당 게시글을 직접 대상으로 한 신고를 반환한다.

### 게시글 노출 상태 변경

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/admin/community/posts/{postId}/visibility` | 관리자 · 콘텐츠처리 | `{"visibility":"HIDDEN","reason":"운영 정책 위반"}` | `200 AdminPostSummary` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 INVALID_CONTENT_TRANSITION | No. 82 · COM-02 · ADM-01 · D08 |

숨김과 복구를 지원한다. 처리자·시각·사유를 기록한다. 숨김 중 댓글 작성과 일반 조회는 차단한다.

### 병원 등록

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/admin/hospitals` | 관리자 · 병원관리 | `{registrationVeterinarianId?,name,businessRegistrationNumber,address,representativeName,detailAddress?,phoneNumber,location?,openingHours?,treatedSpecies?,specialties?}` | `201 AdminHospital` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 HOSPITAL_CONFLICT | No. 35, 83 · ADM-01 · D11 |

가입 시 입력한 병원 정보를 확인하고 등록한다. 병원 중복 기준 및 신청 임시 저장 구조는 미정이다.

### 병원 관리 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/hospitals` | 관리자 · 병원관리 | `keyword(병원명), page, size` | `200 Page<AdminHospital>` | 400 VALIDATION_ERROR | No. 84 · ADM-01 |

운영 권한 내에서 등록 병원을 조회한다.

### 병원 관리 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/hospitals/{hospitalId}` | 관리자 · 병원관리 | `hospitalId` | `200 AdminHospital` | 404 NOT_FOUND | No. 85 · ADM-01 |

위치·연락처·진료 시간·진료 동물·진료 분야를 반환한다. 사업자등록번호와 대표자명은 운영 응답에 포함한다. 좌표·진료 시간·진료 동물·진료 분야 저장 구조는 확인 대상이다.

### 병원 정보 수정

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/admin/hospitals/{hospitalId}` | 관리자 · 병원관리 | `병원 등록 필드 중 변경할 정보(registrationVeterinarianId 제외)` | `200 AdminHospital` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 HOSPITAL_CONFLICT | No. 86 · ADM-01 |

수정된 정보는 지도 및 수의사 소속 병원 응답에 반영한다.

### 병원 정보 삭제

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `DELETE` | `/api/admin/hospitals/{hospitalId}` | 관리자 · 병원관리 | `hospitalId` | `204 본문 없음` | 404 NOT_FOUND, 409 HOSPITAL_IN_USE | No. 87 · ADM-01 |

요구사항은 소프트 삭제다. 소속 수의사와 진행 중 상담에 대한 삭제 허용 조건은 미정이다.

### 결제·환불 내역 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/payments` | 관리자 · 결제관리 | `orderId, caregiverId, transactionType, status, page, size` | `200 Page<AdminPayment>` | 400 VALIDATION_ERROR | PRD ADM-01 · PAY-01·03 · D01·D10 |

환불과 원결제, 충전 주문을 연결한다. 제공사 민감 인증 정보는 반환하지 않는다.

### 코인 원장 운영 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/wallet-transactions` | 관리자 · 코인관리 | `caregiverId, type, relatedId, page, size` | `200 Page<CoinTransaction>` | 400 VALIDATION_ERROR | PRD ADM-01 · PAY-02 |

충전·사용·반환·환불 회수의 관련 주문·상담을 추적한다.

### 수의사 정산 운영 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/settlements` | 관리자 · 정산관리 | `month, veterinarianId, status, page, size` | `200 Page<Settlement>` | 400 VALIDATION_ERROR | PRD ADM-01 · SET-01 · D02 |

대상·부가세 제외 정산 기준액·수수료·병원 지급 계좌 식별자·지급 상태를 대사한다. 실패 대응·수동 재요청 규격과 권한은 D02 확정 후 추가한다.

### 게시판·카테고리 운영 목록

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/admin/community/boards` | 관리자 · 게시판관리 | `page, size` | `200 Page<Board>` | 400 VALIDATION_ERROR | PRD ADM-01 · COM-01 · D08 |

게시판별 카테고리 연결 규칙과 생성·수정·삭제 권한은 미정이다.

## 응답 필드와 데이터 정책

| 응답 타입 | 필드 |
|---|---|
| AdminList<T> | Page<T> + `summary: object`. 회원·수의사: `totalCount, activeCount, inactiveCount`. 신고: `totalCount, resolvedCount, unresolvedCount`. 상담: `totalCount, ongoingCount, delayedCount, cancelledCount, incompleteCount`. 게시글: `totalCount, visibleCount, hiddenCount`. 각 값은 정수 |
| AdminMemberSummary | `memberId: string`, `name: string`, `email: string`, `status: string`. 수의사는 `verificationStatus: string`, `hospital: {hospitalId,name}?` 추가 |
| AdminCaregiver | AdminMemberSummary + `loginId: string`, `phoneNumber: string`, `nickname: string`, `pets: [{petId,name,speciesName,breedName,profileImageUrl}]`, `reportedCount: integer` |
| AdminVeterinarian | AdminMemberSummary의 `hospital`을 AdminHospital로 확장 + `loginId: string`, `phoneNumber: string`, `license: MediaRef?`(인가된 심사자), `payoutAccount: {payoutAccountId,verificationStatus}`(인가된 심사자에게만 제공, 상태값은 D02 미정), `consultationCount: integer`, `reportedCount: integer` |
| ReportSummary | `reportId: string`, `targetType: string`, `targetId: string`, `targetLabel: string`, `authorName: string?`, `reasonCodes: string[]`, `status: string`, `createdAt: datetime` |
| ReportDetail | ReportSummary + `targetContent: string?`, `reporter: {userId,displayName}`, `content: string`, `relatedPostId: integer?`, `relatedCommentId: integer?`, `relatedConsultationId: string?`, `evidence: MediaRef[]`, `resolution: {action,reason,reviewerId,reviewedAt}?` |
| AdminConsultationSummary | ConsultationSummary + `caregiver: {caregiverId,name}`, `hospital: {hospitalId,name}?`, `issues: string[]` |
| AdminPostSummary | PostSummary + `visibility: string` |
| AdminPost | Post + `visibility: string`, `reportCount: integer` |
| AdminHospital | Hospital + `businessRegistrationNumber: string`, `representativeName: string` |
| AdminPayment | `paymentId: string`, `orderId: string`, `caregiverId: string`, `originalPaymentId: string?`, `transactionType: string`, `amountKrw: integer`, `status: string`, `processedAt: datetime?` |
| Board | `boardId: integer`, `name: string`, `categories: [{categoryId,name}]` |

대상별 `targetLabel`은 닉네임, 수의사 이름, 게시글 제목 또는 댓글 내용 일부다. 요약 집계는 조회 영역 기준이며 검색·필터의 집계 적용 범위는 운영 화면과 함께 확정한다. 응답 타입은 [상담](consultation.md), [수의사·병원](veterinarian.md), [커뮤니티](community.md), [결제·정산](payment.md)에서도 정의한다. 관리자 역할과 영역별 권한 매핑은 D05·D08·D11에 따라 확인한다.
