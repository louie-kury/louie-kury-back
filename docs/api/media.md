# API 계약 — 미디어

공통 응답 형식은 [API 명세 안내](README.md)를 참고한다.

---

### 첨부파일 업로드

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/media` | 첨부 목적별 인가된 사용자 | `multipart/form-data. purpose(PET_PROFILE, HEALTH_RECORD, COMMUNITY_POST, REPORT_EVIDENCE), file 1개` | `201 {"mediaId":"media-1","contentType":"image/png","sizeBytes":12040}` | 400 VALIDATION_ERROR, 403 FORBIDDEN, 413 FILE_TOO_LARGE, 415 UNSUPPORTED_MEDIA_TYPE, 503 STORAGE_UNAVAILABLE | No. 12~13, 20~21, 48~49, 72, 74 · HLT-04 · COM-01·02 · D05·D08·D12 |

선업로드 후 대상 생성·수정에 mediaId를 전달한다. 소유자와 업로드 목적이 일치해야 한다. 면허는 수의사 가입 API에서 제출한다. 신고 증빙 업로드 범위와 첨부 개수·형식·용량·임시 보관 기한은 미정이다.

### 첨부파일 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/media/{mediaId}/file` | 연결된 리소스 조회 권한자 | `mediaId` | `200 파일 바이트 및 Content-Type` | 403 FORBIDDEN, 404 NOT_FOUND, 503 STORAGE_UNAVAILABLE | No. 11, 19, 47, 67, 72, 74, 81 · HLT-04 · COM-01·02 · D05·D08·D11 |

요청할 때마다 대상 리소스와 현재 권한을 검사한다. 건강 기록을 공유받은 수의사는 유효한 승인 지정 예약의 범위에서만 열람한다. 즉시 상담 매칭은 기존 건강 기록 첨부파일의 접근 권한을 부여하지 않는다. 면허와 신고 증빙 원본은 별도 관리자 권한을 적용하며 허용 범위는 미정이다.
