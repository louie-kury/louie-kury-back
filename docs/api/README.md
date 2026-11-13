# 루이쿠리 API 명세

요구사항정의서 세 번째 시트의 No. 1~87, [PRD](../prd.md), [ERD](../erd.md)를 기준으로 작성한 API 설계 초안이다. 표의 구성은 [FinPlay API 계약](https://github.com/finplay-team/finplay-backend/tree/dev/docs/api)을 따른다. `No.`는 요구사항정의서 번호다. PRD 기능 ID와 `Dxx`는 제품 정책과 미결정 항목을 가리킨다.

반영 기준 커밋은 PRD `5f03d5b`(수의사 가입과 상담·정산 정책 갱신), ERD `1970283`(최신 PRD 변경 사항을 ERD에 반영)이다. 기존 시트와 충돌하는 소속 병원 선택 및 전화 전용 상담 항목은 최신 PRD 기준으로 갱신했다.

## 도메인별 명세

| 문서 | 엔드포인트 수 |
| --- | --- |
| [계정·인증](auth.md) | 13 |
| [반려동물](pet.md) | 6 |
| [건강 기록](health.md) | 10 |
| [수의사·병원 탐색](veterinarian.md) | 5 |
| [상담·일지·후기](consultation.md) | 21 |
| [미디어](media.md) | 2 |
| [커뮤니티·신고](community.md) | 15 |
| [결제·코인·정산](payment.md) | 8 |
| [관리자](admin.md) | 29 |

## 공통 계약 초안

- 경로는 `/api`를 사용한다. 역할이 지정된 요청은 `Authorization: Bearer <accessToken>`을 사용하고 서버가 계정 역할과 리소스 권한을 확인한다. OAuth 콜백과 재설정처럼 별도 인증이 필요한 요청은 표에 표시한다.
- 성공 표의 JSON과 응답 타입은 공통 성공 응답의 `data`다. 예를 들어 `{"data":{"balanceCoins":7000}}`으로 응답한다. 204, 본문 없음으로 표시한 202, 파일 응답, 302 리다이렉트에는 JSON 래퍼를 사용하지 않는다.
- 오류 응답의 예시는 `{"code":"VALIDATION_ERROR","message":"요청 값이 올바르지 않습니다."}`다. 인증 실패는 401 `UNAUTHORIZED`, 역할·행위 권한 부족은 403 `FORBIDDEN`이다. 본인 소유 또는 당사자만 조회 가능한 객체는 타인의 ID와 없는 ID에 같은 404 `NOT_FOUND`를 반환한다. 표에는 공통 오류 외에 각 API의 주요 오류를 적었다.
- JSON 예시의 입력 필드는 별도 언급이 없으면 필수 초안이다. 요청 필드 이름 뒤 `?`는 생략 가능, 타입 뒤 `?`는 응답에서 `null` 허용을 뜻한다. PATCH에서 생략한 값은 유지하고, 명시적 `null`은 해제가 허용되는 필드만 받는다. 변경 필드가 하나도 없으면 400이다.
- 날짜는 `YYYY-MM-DD`, 시각은 오프셋을 포함한 ISO 8601 형식을 사용한다. 달력의 날짜 경계는 `Asia/Seoul` 초안이다. 예시의 문자열 ID는 불투명 식별자다. 게시글·댓글·종·품종 등 정수 식별자는 해당 문서에 표시한다.
- `Page<T>`는 `{content:T[],page:integer,size:integer,totalElements:integer,totalPages:integer,hasNext:boolean}`이다. `page`는 기본 0, `size`는 기본 20 및 1~100 범위가 초안이다. 빈 목록은 200과 빈 배열을 반환한다.
- `MediaRef`는 `{mediaId:string,url:string,contentType:string}`이다. 파일 URL에서도 현재 접근 권한을 검사한다.
- `Idempotency-Key`가 필수인 API는 호출자와 경로 범위에서 같은 키·같은 입력에 기존 결과를 반환하고, 같은 키에 다른 입력을 쓰면 409 `IDEMPOTENCY_CONFLICT`를 반환한다. 키 보관 기간은 구현 전에 확정한다.

## 정책과 ERD 확인 항목

| 영역 | 확인할 내용 |
| --- | --- |
| 인증·관리자 | 시트의 로그인·소셜 가입·복구 요건은 D11과 함께 확정한다. 시트의 관리자 고정 자격증명 및 관리자 상세 비밀번호 항목은 계약에서 제외했다. 비밀번호 복구는 계정 소유 확인 후 진행한다. |
| 건강 기록 | 복용약·활동 변화·기타 유형과 소프트 삭제는 요구사항 시트 기준이다. ERD 유형·삭제 필드, 관찰 시각과 복용 시각, 타입별 필수값은 D12에서 확인한다. |
| 상담·일지 | 지정 예약과 위치 기반 즉시 상담의 권한·차감 시점을 구분한다. 상담 수단 연동·알림·위치 정책은 D05·D06·D15·D17, 보호자 신고 입력과 일지 수정·삭제는 D04·D07에서 확정한다. |
| 수의사·병원 | 병원 정보·병원 명의 사업자 계좌·면허는 수의사 가입에 필수다. 주소 검색·소속 확인 방식은 D11, 계좌 입력·실명조회 검증 범위는 D02에서 확정한다. |
| 커뮤니티·신고 | 삭제 표시와 신고 조치 범위는 D08에서 확정한다. 상담 완료 시 보호자 신고는 상담과 담당 수의사를 연결한다. 일반 신고 증빙과 게시글·댓글 작성자 키는 추가 확인이 필요하다. |
| 결제·정산 | 7,700원으로 7,000코인을 충전한다. 상담 1건당 7,000코인, 정산 기준 7,000원, 수수료 20%(1,400원), 병원 계좌 지급 5,600원을 적용한다. 외부 통지·환불·지급 실패는 D01·D02·D10에서 확정한다. |

## 최신 PRD에서 추가된 흐름

- [즉시 상담 신청](consultation.md#위치-기반-즉시-상담-신청), [수의사 대기 목록 구독](consultation.md#즉시-상담-대기-목록-구독), [즉시 상담 수락](consultation.md#즉시-상담-수락)
- [상담 연결](consultation.md#상담-연결-요청), [보호자 신고로 상담 완료](consultation.md#보호자-신고로-상담-완료)
- [병원 소속 수의사 가입](auth.md#수의사-가입-및-면허-제출), [병원 명의 계좌 정산](payment.md#내-수의사-정산-목록)

## 요구사항 추적표

| No. | 기능 | 명세 |
| --- | --- | --- |
| 1 | 메인페이지ui | 서비스 소개 UI |
| 2 | 레이아웃 | 헤더 UI와 지도 API. Shop은 v2, [`GET /api/hospitals`](veterinarian.md#지도-병원-목록-조회), [`GET /api/hospitals/{hospitalId}`](veterinarian.md#지도-병원-상세-조회) |
| 3 | 레이아웃 | 푸터와 정적 링크 UI |
| 4 | 일반 로그인 | [`POST /api/auth/login`](auth.md#일반-로그인) |
| 5 | 소셜 로그인 | [`GET /api/auth/oauth/{provider}/authorize`](auth.md#소셜-로그인-시작), [`GET /api/auth/oauth/{provider}/callback`](auth.md#소셜-로그인-콜백) |
| 6 | 아이디찾기 | [`POST /api/auth/login-id/recovery-requests`](auth.md#아이디-찾기-요청) |
| 7 | 비밀번호찾기 | [`POST /api/auth/password/reset-requests`](auth.md#비밀번호-재설정-요청), [`POST /api/auth/password/resets`](auth.md#비밀번호-재설정) |
| 8 | 일반 회원가입 | [`POST /api/auth/caregivers`](auth.md#보호자-일반-가입) |
| 9 | 소셜 회원가입 | [`GET /api/auth/oauth/{provider}/authorize`](auth.md#소셜-로그인-시작), [`GET /api/auth/oauth/{provider}/callback`](auth.md#소셜-로그인-콜백), [`POST /api/auth/oauth/registrations`](auth.md#소셜-가입-완료) |
| 10 | 반려동물 목록 조회 | [`GET /api/pets`](pet.md#반려동물-목록-조회) |
| 11 | 반려동물 상세 조회 | [`GET /api/pets/{petId}`](pet.md#반려동물-상세-조회), [`GET /api/media/{mediaId}/file`](media.md#첨부파일-조회) |
| 12 | 반려동물 등록 | [`POST /api/pets`](pet.md#반려동물-등록), [`GET /api/pet-species`](pet.md#종품종-목록-조회), [`POST /api/media`](media.md#첨부파일-업로드) |
| 13 | 반려동물 정보 수정 | [`PATCH /api/pets/{petId}`](pet.md#반려동물-정보-수정), [`GET /api/pet-species`](pet.md#종품종-목록-조회), [`POST /api/media`](media.md#첨부파일-업로드) |
| 14 | 반려동물 삭제 | [`DELETE /api/pets/{petId}`](pet.md#반려동물-삭제) |
| 15 | 회원 상세 정보 조회 | [`GET /api/members/me`](auth.md#내-회원-상세-조회) |
| 16 | 회원 정보 수정 | [`PATCH /api/members/me`](auth.md#내-회원-정보-수정), [`PUT /api/members/me/password`](auth.md#내-비밀번호-변경) |
| 17 | 회원 탈퇴 | [`DELETE /api/members/me`](auth.md#내-회원-탈퇴) |
| 18 | 건강 기록 목록 조회 | [`GET /api/pets/{petId}/health-records`](health.md#건강-기록-목록-조회), [`GET /api/pets/{petId}/health-records/calendar`](health.md#건강-기록-달력-조회) |
| 19 | 건강 기록 상세 조회 | [`GET /api/pets/{petId}/health-records/{recordId}`](health.md#건강-기록-상세-조회), [`GET /api/media/{mediaId}/file`](media.md#첨부파일-조회) |
| 20 | 일자 및 상태 기록 | [`POST /api/pets/{petId}/health-records`](health.md#건강-기록-등록), [`POST /api/media`](media.md#첨부파일-업로드) |
| 21 | 건강 기록 정보 수정 | [`PATCH /api/pets/{petId}/health-records/{recordId}`](health.md#건강-기록-수정), [`POST /api/media`](media.md#첨부파일-업로드) |
| 22 | 건강 기록 삭제 | [`DELETE /api/pets/{petId}/health-records/{recordId}`](health.md#건강-기록-삭제) |
| 23 | 수의사 목록 조회 | [`GET /api/veterinarians`](veterinarian.md#수의사-목록-조회) |
| 24 | 수의사 상세 조회 | [`GET /api/veterinarians/{veterinarianId}`](veterinarian.md#수의사-상세-조회), [`GET /api/hospitals/{hospitalId}`](veterinarian.md#지도-병원-상세-조회) |
| 25 | 반려동물 선택 | [`GET /api/pets`](pet.md#반려동물-목록-조회), [`POST /api/consultations`](consultation.md#지정-수의사-예약-요청) |
| 26 | 상담 내용 작성 | [`POST /api/consultations`](consultation.md#지정-수의사-예약-요청) |
| 27 | 상담 신청 및 수단 선택 | [`POST /api/consultations`](consultation.md#지정-수의사-예약-요청), [`POST /api/consultations/{consultationId}/connections`](consultation.md#상담-연결-요청) |
| 28 | 메인페이지ui | 서비스 소개 UI |
| 29 | 레이아웃 | 수의사 헤더 UI |
| 30 | 레이아웃 | 푸터와 정적 링크 UI |
| 31 | 로그인 | [`POST /api/auth/login`](auth.md#일반-로그인) |
| 32 | 아이디찾기 | [`POST /api/auth/login-id/recovery-requests`](auth.md#아이디-찾기-요청) |
| 33 | 비밀번호 찾기 | [`POST /api/auth/password/reset-requests`](auth.md#비밀번호-재설정-요청), [`POST /api/auth/password/resets`](auth.md#비밀번호-재설정) |
| 34 | 회원가입 정보 입력 | [`POST /api/auth/veterinarians`](auth.md#수의사-가입-및-면허-제출) |
| 35 | 병원정보 등록 | [`POST /api/auth/veterinarians`](auth.md#수의사-가입-및-면허-제출), [`POST /api/admin/hospitals`](admin.md#병원-등록) |
| 36 | 수의사 면허 등록 | [`POST /api/auth/veterinarians`](auth.md#수의사-가입-및-면허-제출) |
| 37 | 회원 상세 정보 조회 | [`GET /api/members/me`](auth.md#내-회원-상세-조회) |
| 38 | 회원 정보 수정 | [`PATCH /api/members/me`](auth.md#내-회원-정보-수정), [`PUT /api/members/me/password`](auth.md#내-비밀번호-변경) |
| 39 | 회원 탈퇴 | [`DELETE /api/members/me`](auth.md#내-회원-탈퇴) |
| 40 | 신규 상담 요청 목록 조회 | [`GET /api/consultations`](consultation.md#내-상담-목록-조회) |
| 41 | 신규 상담 요청 상세 조회 | [`GET /api/consultations/{consultationId}`](consultation.md#내-상담-상세-조회) |
| 42 | 완료된 상담 목록 조회 | [`GET /api/consultations`](consultation.md#내-상담-목록-조회) |
| 43 | 완료된 상담 상세 조회 | [`GET /api/consultations/{consultationId}`](consultation.md#내-상담-상세-조회) |
| 44 | 상담 일지 작성 | [`POST /api/consultations/{consultationId}/journal`](consultation.md#상담-일지-작성) |
| 45 | 상담 일지 수정 | [`PATCH /api/consultations/{consultationId}/journal`](consultation.md#상담-일지-수정) |
| 46 | 게시물 목록 조회 | [`GET /api/community/posts`](community.md#게시글-목록-조회) |
| 47 | 게시물 상세 조회 | [`GET /api/media/{mediaId}/file`](media.md#첨부파일-조회), [`GET /api/community/posts/{postId}`](community.md#게시글-상세-조회), [`GET /api/community/posts/{postId}/comments`](community.md#댓글대댓글-목록-조회) |
| 48 | 게시물 작성 | [`POST /api/media`](media.md#첨부파일-업로드), [`POST /api/community/posts`](community.md#게시글-작성) |
| 49 | 게시물 수정 | [`POST /api/media`](media.md#첨부파일-업로드), [`PATCH /api/community/posts/{postId}`](community.md#게시글-수정) |
| 50 | 게시물 삭제 | [`DELETE /api/community/posts/{postId}`](community.md#게시글-삭제) |
| 51 | 게시물 좋아요 | [`PUT /api/community/posts/{postId}/likes/me`](community.md#게시글-좋아요-표시), [`DELETE /api/community/posts/{postId}/likes/me`](community.md#게시글-좋아요-취소) |
| 52 | 댓글 작성 | [`GET /api/community/posts/{postId}/comments`](community.md#댓글대댓글-목록-조회), [`POST /api/community/posts/{postId}/comments`](community.md#댓글대댓글-작성) |
| 53 | 댓글 수정 | [`PATCH /api/community/posts/{postId}/comments/{commentId}`](community.md#댓글-수정) |
| 54 | 댓글 삭제 | [`GET /api/community/posts/{postId}/comments`](community.md#댓글대댓글-목록-조회), [`DELETE /api/community/posts/{postId}/comments/{commentId}`](community.md#댓글-삭제) |
| 55 | 댓글 좋아요 | [`PUT /api/community/posts/{postId}/comments/{commentId}/likes/me`](community.md#댓글-좋아요-표시), [`DELETE /api/community/posts/{postId}/comments/{commentId}/likes/me`](community.md#댓글-좋아요-취소) |
| 56 | 게시물 신고 | [`GET /api/reports/reasons`](community.md#신고-사유-목록-조회), [`POST /api/reports`](community.md#게시글댓글사용자-신고-접수) |
| 57 | 댓글 신고 | [`GET /api/reports/reasons`](community.md#신고-사유-목록-조회), [`POST /api/reports`](community.md#게시글댓글사용자-신고-접수) |
| 58 | 사용자 신고 | [`GET /api/reports/reasons`](community.md#신고-사유-목록-조회), [`POST /api/reports`](community.md#게시글댓글사용자-신고-접수) |
| 59 | 로그인 | [`POST /api/auth/login`](auth.md#일반-로그인) |
| 60 | 비밀번호 초기화 | [`POST /api/auth/password/reset-requests`](auth.md#비밀번호-재설정-요청), [`POST /api/auth/password/resets`](auth.md#비밀번호-재설정) |
| 61 | 전체 상태 요약 | [`GET /api/admin/dashboard`](admin.md#운영-대시보드-조회) |
| 62 | 일반 회원 목록 조회 | [`GET /api/admin/caregivers`](admin.md#일반-회원-목록-조회) |
| 63 | 일반 회원 상세 조회 | [`GET /api/admin/caregivers/{caregiverId}`](admin.md#일반-회원-상세-조회) |
| 64 | 일반 회원 상태 관리 | [`PATCH /api/admin/caregivers/{caregiverId}/status`](admin.md#일반-회원-상태-변경) |
| 65 | 수의사 인증 관리 | [`GET /api/admin/veterinarians`](admin.md#수의사-목록-조회), [`GET /api/admin/veterinarians/{veterinarianId}`](admin.md#수의사-상세-조회), [`PATCH /api/admin/veterinarians/{veterinarianId}/verification`](admin.md#수의사-인증-심사) |
| 66 | 수의사 목록 조회 | [`GET /api/admin/veterinarians`](admin.md#수의사-목록-조회) |
| 67 | 수의사 상세 조회 | [`GET /api/media/{mediaId}/file`](media.md#첨부파일-조회), [`GET /api/admin/veterinarians/{veterinarianId}`](admin.md#수의사-상세-조회) |
| 68 | 수의사 상태 관리 | [`PATCH /api/admin/veterinarians/{veterinarianId}/status`](admin.md#수의사-계정-상태-변경) |
| 69 | 사용자 신고 접수 목록 조회 | [`GET /api/admin/reports`](admin.md#신고-접수-목록-조회) |
| 70 | 사용자 신고 접수 상세 조회 | [`GET /api/admin/reports/{reportId}`](admin.md#신고-접수-상세-조회), [`PATCH /api/admin/reports/{reportId}/resolution`](admin.md#신고-검토-및-처리) |
| 71 | 수의사 신고 접수 목록 조회 | [`GET /api/admin/reports`](admin.md#신고-접수-목록-조회) |
| 72 | 수의사 신고 접수 상세 조회 | [`POST /api/media`](media.md#첨부파일-업로드), [`GET /api/media/{mediaId}/file`](media.md#첨부파일-조회), [`GET /api/admin/reports/{reportId}`](admin.md#신고-접수-상세-조회), [`PATCH /api/admin/reports/{reportId}/resolution`](admin.md#신고-검토-및-처리) |
| 73 | 게시물 신고 접수 목록 조회 | [`GET /api/admin/reports`](admin.md#신고-접수-목록-조회) |
| 74 | 게시물 신고 접수 상세 조회 | [`POST /api/media`](media.md#첨부파일-업로드), [`GET /api/media/{mediaId}/file`](media.md#첨부파일-조회), [`GET /api/admin/reports/{reportId}`](admin.md#신고-접수-상세-조회), [`PATCH /api/admin/reports/{reportId}/resolution`](admin.md#신고-검토-및-처리) |
| 75 | 댓글 신고 접수 목록 조회 | [`GET /api/admin/reports`](admin.md#신고-접수-목록-조회) |
| 76 | 댓글 신고 접수 상세 조회 | [`GET /api/admin/reports/{reportId}`](admin.md#신고-접수-상세-조회), [`PATCH /api/admin/reports/{reportId}/resolution`](admin.md#신고-검토-및-처리) |
| 77 | 상담 목록 조회 | [`GET /api/admin/consultations`](admin.md#상담-목록-조회) |
| 78 | 상담 일지 조회 | [`GET /api/admin/consultations/{consultationId}/journal`](admin.md#상담-일지-조회) |
| 79 | 상담일지 삭제 | [`DELETE /api/admin/consultations/{consultationId}/journal`](admin.md#상담-일지-삭제) |
| 80 | 게시물 목록 조회 | [`GET /api/admin/community/posts`](admin.md#게시글-관리-목록-조회) |
| 81 | 게시물 상세 조회 | [`GET /api/media/{mediaId}/file`](media.md#첨부파일-조회), [`GET /api/admin/community/posts/{postId}`](admin.md#게시글-관리-상세-조회), [`GET /api/admin/community/posts/{postId}/comments`](admin.md#게시글-관리-댓글-조회), [`GET /api/admin/community/posts/{postId}/reports`](admin.md#게시글-관리-신고-이력-조회) |
| 82 | 게시물 상태 관리 | [`PATCH /api/admin/community/posts/{postId}/visibility`](admin.md#게시글-노출-상태-변경) |
| 83 | 병원 등록 관리 | [`POST /api/admin/hospitals`](admin.md#병원-등록) |
| 84 | 병원 목록 조회 | [`GET /api/admin/hospitals`](admin.md#병원-관리-목록-조회) |
| 85 | 병원 상세 조회 | [`GET /api/admin/hospitals/{hospitalId}`](admin.md#병원-관리-상세-조회) |
| 86 | 병원 정보 수정 | [`PATCH /api/admin/hospitals/{hospitalId}`](admin.md#병원-정보-수정) |
| 87 | 병원 정보 삭제 | [`DELETE /api/admin/hospitals/{hospitalId}`](admin.md#병원-정보-삭제) |
