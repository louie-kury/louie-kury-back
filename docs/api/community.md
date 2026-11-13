# API 계약 — 커뮤니티·신고

공통 응답 형식은 [API 명세 안내](README.md)를 참고한다.

---

### 게시글 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/community/posts` | 보호자·활동 가능한 수의사 | `boardId, categoryId, page, size` | `200 Page<PostSummary>` | 400 VALIDATION_ERROR | No. 46 · COM-01 · D08 |

일반 화면에는 노출 가능한 게시글만 반환한다. 비로그인 열람 및 게시판별 권한은 미정이다.

### 게시글 상세 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/community/posts/{postId}` | 보호자·활동 가능한 수의사 | `postId` | `200 Post` | 404 NOT_FOUND | No. 47 · COM-01 · D08 |

댓글은 같은 postId의 댓글 목록 API에서 조회한다.

### 게시글 작성

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/community/posts` | 보호자·활동 가능한 수의사 | `{"boardId":1,"categoryId":2,"title":"루이 산책","content":"오늘 산책을 다녀왔어요.","mediaIds":["media-1"]}` | `201 Post` | 400 VALIDATION_ERROR, 403 FORBIDDEN, 404 NOT_FOUND | No. 48 · COM-01 · D08 |

title·content는 필수, mediaIds는 선택 초안이다. 사진과 동영상 첨부를 지원하며 게시판·카테고리 필수 여부와 첨부 제한은 미정이다.

### 게시글 수정

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/community/posts/{postId}` | 작성자 | `{title?,content?,mediaIds?}` | `200 Post` | 400 VALIDATION_ERROR, 403 FORBIDDEN, 404 NOT_FOUND | No. 49 · COM-01 · D08 |

mediaIds가 있으면 첨부 목록을 교체한다. 빈 배열은 모든 첨부 해제를 요청한다.

### 게시글 삭제

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `DELETE` | `/api/community/posts/{postId}` | 작성자 | `postId` | `204 본문 없음` | 403 FORBIDDEN, 404 NOT_FOUND | No. 50 · COM-01 · D08 |

요구사항은 소프트 삭제다. 삭제된 글은 일반 조회와 신규 댓글 작성 대상에서 제외된다. 댓글·첨부 보존은 미정이다.

### 게시글 좋아요 표시

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PUT` | `/api/community/posts/{postId}/likes/me` | 보호자·활동 가능한 수의사 | `postId, 본문 없음` | `200 {"likeCount":1,"likedByMe":true}` | 404 NOT_FOUND | No. 51 · COM-01 · D08 |

동일 사용자의 중복 요청으로 수가 증가하지 않는다.

### 게시글 좋아요 취소

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `DELETE` | `/api/community/posts/{postId}/likes/me` | 보호자·활동 가능한 수의사 | `postId` | `204 본문 없음` | 404 NOT_FOUND | No. 51 · COM-01 · D08 |

취소 API는 초안이다. 취소 가능 여부 및 운영 정책은 미정이다.

### 댓글·대댓글 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/community/posts/{postId}/comments` | 보호자·활동 가능한 수의사 | `postId, page, size` | `200 Page<Comment>` | 400 VALIDATION_ERROR, 404 NOT_FOUND | No. 47, 52, 54 · COM-01 · D08 |

parentCommentId로 계층을 연결한다. 요구사항의 삭제 표시 문구는 “삭제된 댓글입니다”다. 부모 삭제 후 대댓글 표시와 페이지 경계 규칙은 미정이다.

### 댓글·대댓글 작성

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/community/posts/{postId}/comments` | 보호자·활동 가능한 수의사 | `{"content":"산책 좋죠!","parentCommentId":null}` | `201 Comment` | 400 VALIDATION_ERROR, 404 NOT_FOUND, 409 COMMENTS_CLOSED | No. 52 · COM-01 · D08 |

content는 필수다. parentCommentId는 선택이며 같은 글에 속해야 한다. 최대 깊이와 삭제된 부모에 대한 답글 허용은 미정이다.

### 댓글 수정

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PATCH` | `/api/community/posts/{postId}/comments/{commentId}` | 작성자 | `{"content":"산책하기 좋은 날이네요."}` | `200 Comment` | 400 VALIDATION_ERROR, 403 FORBIDDEN, 404 NOT_FOUND | No. 53 · COM-01 · D08 |

작성자와 게시글-댓글 관계를 검사한다.

### 댓글 삭제

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `DELETE` | `/api/community/posts/{postId}/comments/{commentId}` | 작성자 | `postId, commentId` | `204 본문 없음` | 403 FORBIDDEN, 404 NOT_FOUND | No. 54 · COM-01 · D08 |

삭제 표시를 반환하는 경우 원문은 일반 응답에서 제외한다.

### 댓글 좋아요 표시

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `PUT` | `/api/community/posts/{postId}/comments/{commentId}/likes/me` | 보호자·활동 가능한 수의사 | `postId, commentId, 본문 없음` | `200 {"likeCount":1,"likedByMe":true}` | 404 NOT_FOUND | No. 55 · COM-01 · D08 |

동일 사용자의 중복 요청으로 수가 증가하지 않는다.

### 댓글 좋아요 취소

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `DELETE` | `/api/community/posts/{postId}/comments/{commentId}/likes/me` | 보호자·활동 가능한 수의사 | `postId, commentId` | `204 본문 없음` | 404 NOT_FOUND | No. 55 · COM-01 · D08 |

취소 API는 초안이다. 취소 가능 여부 및 운영 정책은 미정이다.

### 신고 사유 목록 조회

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `GET` | `/api/reports/reasons` | 보호자·활동 가능한 수의사 | `targetType 필수(CAREGIVER, VETERINARIAN, POST, COMMENT)` | `200 [{"code":"SPAM","name":"광고 또는 도배"}]` | 400 VALIDATION_ERROR | No. 56~58 · COM-02 · D08 |

신고 대상에 활성화된 사유만 반환한다. 예시 코드는 실제 운영 분류와 함께 확정한다.

### 게시글·댓글·사용자 신고 접수

| Method | URL | 인증 | 요청 | 성공 응답 | 오류 응답 | Spec |
| --- | --- | --- | --- | --- | --- | --- |
| `POST` | `/api/reports` | 보호자·활동 가능한 수의사 | `{"targetType":"POST","targetId":"21","reasonCodes":["SPAM"],"content":"반복 광고입니다.","evidenceMediaIds":[]}` | `201 {"reportId":"report-1","status":"RECEIVED"}` | 400 VALIDATION_ERROR, 403 FORBIDDEN, 404 NOT_FOUND | No. 56~58 · COM-02 · D08 |

targetType과 targetId의 조합으로 대상을 검증한다. 신고 대상에게 신고자 정보를 공개하지 않는다. 일반 신고의 중복 처리와 증빙 범위는 D08에서 확정한다. 상담 완료 확인창에서 담당 수의사가 해당 보호자를 신고하는 흐름은 [상담 완료와 보호자 신고](consultation.md#보호자-신고로-상담-완료)를 사용한다.

## 응답 필드와 데이터 정책

| 응답 타입 | 필드 |
|---|---|
| Author | `userId: string`, `displayName: string`, `veterinarianBadge: boolean` |
| PostSummary | `postId: integer`, `author: Author`, `title: string`, `createdAt: datetime`, `likeCount: integer`, `likedByMe: boolean`, `commentCount: integer` |
| Post | PostSummary + `content: string`, `updatedAt: datetime?`, `boardId: integer`, `categoryId: integer`, `media: MediaRef[]` |
| Comment | `commentId: integer`, `parentCommentId: integer?`, `author: Author?`, `content: string`, `deleted: boolean`, `createdAt: datetime`, `updatedAt: datetime?`, `likeCount: integer`, `likedByMe: boolean` |

수의사 표시는 승인 상태에 따라 결정한다. 신고 요청의 `targetId`는 문자열이다. 게시글·댓글에는 해당 정수 ID의 문자열 표현을 사용한다. API의 `POST` 대상과 ERD의 `BOARD` 상태명 매핑은 확인 대상이다. `targetType`, `targetId`, `reasonCodes`는 필수 초안이며 `content`와 `evidenceMediaIds`는 선택 초안이다.
