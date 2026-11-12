# ERD (Entity Relationship Diagram)

루이쿠리의 현재 ERD 초안을 도메인별로 정리했다. 테이블명, 컬럼명, 타입, NULL 허용 여부와 주석은 첨부 SQL을 기준으로 한다. 제품 요구사항은 [PRD](prd.md)에서 확인할 수 있다.

- `PK`는 첨부 SQL에 선언된 기본키이며, `NULL` 표기가 없는 컬럼은 `NOT NULL`이다.
- 점선은 컬럼명에서 추정한 참조 관계다. 관계의 개수는 참조 컬럼의 NULL 허용 여부를 바탕으로 표시했다. 첨부 SQL에는 FK와 UNIQUE 제약 선언이 없다.
- 다른 도메인의 참조 대상은 해당 다이어그램에 이름만 표시한다.

## 엔티티 목록

| 도메인 | 테이블 |
| --- | --- |
| 계정 · 인증 | `계정` |
| 계정 · 인증 | `로그인기록` |
| 계정 · 인증 | `소셜인증` |
| 보호자 · 수의사 · 병원 | `보호자` |
| 보호자 · 수의사 · 병원 | `보호자 미디어` |
| 보호자 · 수의사 · 병원 | `보호자 약관` |
| 보호자 · 수의사 · 병원 | `보호자 약관 동의` |
| 보호자 · 수의사 · 병원 | `수의사` |
| 보호자 · 수의사 · 병원 | `수의사 미디어` |
| 보호자 · 수의사 · 병원 | `수의사 약관` |
| 보호자 · 수의사 · 병원 | `수의사 약관 동의` |
| 보호자 · 수의사 · 병원 | `병원` |
| 반려동물 · 건강 기록 | `반려동물` |
| 반려동물 · 건강 기록 | `종` |
| 반려동물 · 건강 기록 | `품종` |
| 반려동물 · 건강 기록 | `미디어` |
| 반려동물 · 건강 기록 | `건강기록` |
| 반려동물 · 건강 기록 | `건강기록상세` |
| 반려동물 · 건강 기록 | `건강기록미디어` |
| 반려동물 · 건강 기록 | `예방접종` |
| 반려동물 · 건강 기록 | `접종명` |
| 반려동물 · 건강 기록 | `병원진료` |
| 상담 · 일지 · 후기 | `상담` |
| 코인 · 결제 · 정산 | `코인 지갑` |
| 코인 · 결제 · 정산 | `코인 충전 주문` |
| 코인 · 결제 · 정산 | `코인 결제` |
| 코인 · 결제 · 정산 | `코인 내역` |
| 코인 · 결제 · 정산 | `상담 코인 홀드` |
| 코인 · 결제 · 정산 | `수의사 정산` |
| 커뮤니티 | `유저정보` |
| 커뮤니티 | `게시판` |
| 커뮤니티 | `카테고리` |
| 커뮤니티 | `게시글` |
| 커뮤니티 | `게시글 미디어` |
| 커뮤니티 | `게시글 좋아요` |
| 커뮤니티 | `댓글` |
| 커뮤니티 | `댓글 좋아요` |
| 관리자 · 신고 | `관리자` |
| 관리자 · 신고 | `권한` |
| 관리자 · 신고 | `관리자권한` |
| 관리자 · 신고 | `신고` |
| 관리자 · 신고 | `신고 사유` |
| 관리자 · 신고 | `신고 사유 선정` |

## 1. 계정 · 인증

```mermaid
erDiagram
    "계정" ||..o{ "로그인기록" : "Auth_id"
    "계정" ||..o{ "소셜인증" : "Auth_id"

    "계정" {
        BIGINT id PK
        VARCHAR user_UUID
        VARCHAR type "보호자/수의사/관리자  구분"
        VARCHAR login_id
        VARCHAR password "NULL · 소셜 로그인시 null"
        VARCHAR status "가입 대기, 활동, 탈퇴, 정지(Enum으로 관리)"
        DATETIME created_at
        DATETIME updated_at
        DATETIME deleted_at
    }
    "로그인기록" {
        BIGINT id PK
        BIGINT Auth_id
        VARCHAR login_type
        DATETIME fail_reason "NULL"
        INTEGER login_attempt "NULL"
        BOOLEAN is_successed
        DATETIME authenticated_at
    }
    "소셜인증" {
        BIGINT id PK
        BIGINT Auth_id
        VARCHAR provider
        VARCHAR provider_user_id
        DATETIME authenticated_at
        DATETIME deleted_at
    }
```

`계정.user_UUID`의 참조 대상은 `type`에 따라 보호자·수의사·관리자로 달라지는 것으로 보인다. 역할별 UUID 연결 방식과 유일성은 확인이 필요하다.

## 2. 보호자 · 수의사 · 병원

```mermaid
erDiagram
    "보호자" ||..o{ "보호자 미디어" : "caregiver_id"
    "보호자" ||..o{ "보호자 약관 동의" : "caregiver_id"
    "보호자 약관" ||..o{ "보호자 약관 동의" : "terms_id"
    "수의사" ||..o{ "수의사 미디어" : "veterinarian_id"
    "병원" ||..o{ "수의사" : "hospital_id"

    "보호자" {
        BIGINT id PK
        VARCHAR uuid
        VARCHAR(50) name
        VARCHAR(20) phone_number
        VARCHAR(20) email
        VARCHAR(30) nick_name
        DATETIME created_at
        DATETIME updated_at
        DATETIME deleted_at "NULL"
    }
    "보호자 미디어" {
        BIGINT id PK
        BIGINT caregiver_id
        VARCHAR file_name
        VARCHAR(10) media_type
        VARCHAR(45) file_extension
        INTEGER file_size
        VARCHAR(255) media_url
        DATETIME created_at
        DATETIME updated_at
        DATETIME deleted_at "NULL"
    }
    "보호자 약관" {
        BIGINT id PK
        VARCHAR title
        VARCHAR content
        BOOLEAN required
        DATETIME created_at
        VARCHAR version
    }
    "보호자 약관 동의" {
        BIGINT id PK
        BIGINT caregiver_id
        BIGINT terms_id
        BOOLEAN agreed
        DATETIME agreed_at
    }
    "수의사" {
        BIGINT id PK
        BIGINT hospital_id
        VARCHAR uuid
        VARCHAR hospital_uuid "NULL"
        VARCHAR(50) name
        VARCHAR(20) phone_number
        VARCHAR(20) email
        DATETIME created_at
        DATETIME updated_at
        DATETIME deletd_at "NULL"
        VARCHAR status
        DOUBLE rating "평균평점"
    }
    "수의사 미디어" {
        BIGINT id PK
        BIGINT veterinarian_id
        VARCHAR file_name
        VARCHAR(10) media_type "수의사 면허 타입도 관리"
        VARCHAR(45) file_extension
        INTEGER file_size
        VARCHAR(255) media_url
        DATETIME created_at
        DATETIME updated_at "NULL"
        DATETIME deleted_at "NULL"
    }
    "수의사 약관" {
        BIGINT id PK
        VARCHAR title
        VARCHAR content
        BOOLEAN required
        DATETIME created_at
    }
    "수의사 약관 동의" {
        VARCHAR(255) id PK
        BIGINT veterinarian_uuid
        BIGINT id2
        BOOLEAN agreed
        DATETIME agreed_at
    }
    "병원" {
        BIGINT id PK
        VARCHAR(255) uuid
        VARCHAR name
        VARCHAR address
        VARCHAR detail_address
        VARCHAR tel_no
        DATETIME created_at
        DATETIME updated_at
        DATETIME deleted_at "NULL"
    }
```

`수의사`에는 `hospital_id`와 `hospital_uuid`가 함께 있다. `수의사 약관 동의.veterinarian_uuid`는 `BIGINT`이고 `수의사.uuid`는 `VARCHAR`다. `veterinarian_uuid`와 `id2`의 참조 대상 컬럼을 확인해야 한다.

## 3. 반려동물 · 건강 기록

```mermaid
erDiagram
    "보호자" ||..o{ "반려동물" : "caregiver_uuid"
    "종" ||..o{ "품종" : "species_id"
    "종" ||..o{ "반려동물" : "species_id"
    "품종" ||..o{ "반려동물" : "breed_id"
    "반려동물" ||..o{ "미디어" : "pet_id"
    "반려동물" ||..o{ "건강기록" : "pet_uuid"
    "반려동물" ||..o{ "예방접종" : "pet_id"
    "반려동물" ||..o{ "병원진료" : "pet_id"
    "건강기록" ||..o{ "건강기록상세" : "health_record_id"
    "건강기록" ||..o{ "건강기록미디어" : "health_record_id"

    "반려동물" {
        BIGINT id PK
        BIGINT species_id
        BIGINT breed_id
        VARCHAR(100) uuid
        VARCHAR caregiver_uuid
        VARCHAR(50) name
        DATE birth "NULL"
        BOOLEAN sex
        BOOLEAN is_neutered "NULL"
        DOUBLE weight "DOUBLE(19,2) · NULL"
        BOOLEAN vaccination "NULL"
        DATETIME created_at
        DATETIME updated_at
        DATETIME deleted_at "NULL"
    }
    "종" {
        BIGINT id PK
        VARCHAR(50) name
    }
    "품종" {
        BIGINT id PK
        BIGINT species_id
        VARCHAR(50) name
    }
    "미디어" {
        BIGINT id PK
        BIGINT pet_id
        VARCHAR title
        VARCHAR(10) media_type
        VARCHAR(45) file_extension
        INTEGER file_size
        VARCHAR(255) media_url
        DATETIME created_at
        DATETIME updated_at "NULL"
        DATETIME deleted_at "NULL"
    }
    "건강기록" {
        BIGINT id PK
        VARCHAR pet_uuid
        VARCHAR type "Enum(음수량, 구토, 체중, 변, 식사량, 상처)"
        DATETIME evented_at
        DATETIME created_at
        DATETIME updated_at
    }
    "건강기록상세" {
        VARCHAR(255) id PK
        BIGINT health_record_id
        VARCHAR sub_type "NULL · 변모양, 변색깔, 구토색깔"
        VARCHAR text_content "NULL"
        DOUBLE numeric_content "NULL · 액체량, 식사량"
    }
    "건강기록미디어" {
        BIGINT id PK
        BIGINT health_record_id
        VARCHAR file_name
        VARCHAR(10) media_type
        VARCHAR(45) file_extension
        INTEGER file_size
        VARCHAR(255) media_url
        DATETIME created_at
        DATETIME updated_at "NULL"
        DATETIME deleted_at "NULL"
    }
    "예방접종" {
        VARCHAR(255) id PK
        BIGINT pet_id
        BIGINT vaccine_name_id
        DATETIME evented_at
        DATETIME created_at
        DATETIME updated_at
    }
    "접종명" {
        VARCHAR(255) id PK
        VARCHAR(255) name
        VARCHAR(255) created_at
    }
    "병원진료" {
        VARCHAR(255) id PK
        BIGINT pet_id
        DATETIME visited_at
        VARCHAR type
        VARCHAR content
        DATETIME evented_at
        DATETIME created_at
        DATETIME updated_at
    }
```

`예방접종.vaccine_name_id`의 참조 후보는 `접종명.id`다. 두 타입이 각각 `BIGINT`와 `VARCHAR(255)`이므로 연결 전에 참조 키와 타입을 확인해야 한다.

## 4. 상담 · 일지 · 후기

```mermaid
erDiagram
    "보호자" ||..o{ "상담" : "caregiver_uuid"
    "수의사" ||..o{ "상담" : "veterinarian_uuid"
    "반려동물" ||..o{ "상담" : "pet_uuid"

    "상담" {
        BIGINT id PK
        VARCHAR uuid
        VARCHAR caregiver_uuid
        VARCHAR veterinarian_uuid
        VARCHAR pet_uuid
        VARCHAR status "대기, 상담중, 완료"
        VARCHAR consultation_title
        VARCHAR consultation_content
        VARCHAR consultation_record "내용만 작성"
        DOUBLE rating "NULL"
        VARCHAR review_content "NULL"
        DATETIME created_at
        DATETIEM preferred_at "NULL"
        DATETIME consulted_at "NULL"
        DATETIME cancelled_at "NULL"
        DATETIME reviewed_at "NULL"
    }
```

첨부본은 상담 일지와 후기 정보를 `상담.consultation_record`, `rating`, `review_content`, `reviewed_at`에 담는다. `preferred_at`의 타입은 원본에 `DATETIEM`으로 적혀 있다.

## 5. 코인 · 결제 · 정산

```mermaid
erDiagram
    "보호자" ||..o{ "코인 지갑" : "caregiver_uuid"
    "보호자" ||..o{ "코인 충전 주문" : "caregiver_uuid"
    "코인 지갑" ||..o{ "코인 충전 주문" : "coin_wallet_id"
    "코인 충전 주문" ||..o{ "코인 결제" : "charge_order_id"
    "코인 지갑" ||..o{ "코인 내역" : "wallet_id"
    "코인 지갑" ||..o{ "상담 코인 홀드" : "wallet_id"
    "상담" ||..o{ "상담 코인 홀드" : "consultation_uuid"
    "보호자" ||..o{ "상담 코인 홀드" : "caregiver_uuid"
    "상담 코인 홀드" ||..o{ "수의사 정산" : "consultation_hold_id"
    "수의사" ||..o{ "수의사 정산" : "veterinarian_UUID"

    "코인 지갑" {
        BIGINT id PK
        VARCHAR(255) uuid "NULL"
        VARCHAR caregiver_uuid
        INTEGER balance
        DATETIME created_at
        DATETIME updated_at
    }
    "코인 충전 주문" {
        BIGINT id PK
        BIGINT coin_wallet_id
        VARCHAR order_uuid
        VARCHAR caregiver_uuid
        INTEGER charge_amount
        VARCHAR status
        DATETIME created_at
        DATETIME expires_at
        DATETIME updated_at "ENUM(PENDING, PAID, CANCELLED, FAILED, EXPIRED)"
        VARCHAR remark "NULL"
    }
    "코인 결제" {
        BIGINT id PK
        BIGINT charge_order_id
        INTEGER original_transaction_id "NULL · FK -> coin_payment_transaction.id, 환불 시 원본 결제 참조"
        VARCHAR pg_payment_key "NULL · PG사에서 발급한 결제 식별자 UNIQUE"
        VARCHAR pg_cancel_key "NULL · PG사에서 발급한 취소 식별자"
        VARCHAR transaction_type "Enum(PAYMENT, REFUND)"
        INTEGER amount "결제는 양수(+), 환불은 음수(-)"
        VARCHAR method "카드, 간편결제"
        VARCHAR status "ENUM(PENDING, PAID, CANCELLED, FAILED, EXPIRED)"
        DATETIME paid_at "NULL · 결제 승인 또는 환불 완료 일시"
        DATETIME created_at
        DATETIME updated_at
        VARCHAR remark "NULL"
        VARCHAR refund_type "ENUM"
        VARCHAR refund_reason
    }
    "코인 내역" {
        BIGINT id PK
        BIGINT wallet_id
        VARCHAR transaction_type
        INTEGER coin_amount
        INTEGER balance_after
        VARCHAR related_type "ENUM(결제, 홀드, 환불)"
        BIGINT related_id
        VARCHAR description "NULL"
        DATETIME created_at
    }
    "상담 코인 홀드" {
        BIGINT id PK
        BIGINT wallet_id
        VARCHAR consultation_uuid
        VARCHAR caregiver_uuid
        INTEGER hold_coint_amount
        VARCHAR status "ENUM(HEILD, RELEASED, USED)"
        DATETIME created_at
        DATETIME released_at "NULL"
        DATETIME used_at "NULL"
    }
    "수의사 정산" {
        BIGINT id PK
        BIGINT consultation_hold_id
        VARCHAR veterinarian_UUID
        INTEGER coin_amount
        DECIMAL commision_rate "DECIMAL(5, 2) · BIGDECIMAL"
        INTEGER comission_amount
        INTEGER payout_amount
        VARCHAR status "ENUM(PENDING, READY, PAID, CANCELLED)"
        DATETIME paid_at "NULL"
        DATETIME created_at
    }
```

`코인 결제.original_transaction_id`의 원본 주석은 결제 자기 참조를 가리킨다. 이 컬럼은 `INTEGER`이고 `코인 결제.id`는 `BIGINT`다. `pg_payment_key`의 유일성은 주석에 기재돼 있다. `코인 내역.related_type`과 `related_id`의 대상 테이블은 유형별로 확인해야 한다.

## 6. 커뮤니티

```mermaid
erDiagram
    "게시판" ||..o{ "게시글" : "board_id"
    "카테고리" ||..o{ "게시글" : "category_id"
    "게시글" ||..o{ "게시글 미디어" : "post_id"
    "게시글" ||..o{ "게시글 좋아요" : "post_id"
    "게시글" ||..o{ "댓글" : "post_id"
    "댓글" |o..o{ "댓글" : "parent_comment_id"
    "댓글" ||..o{ "댓글" : "root_comment_id"
    "댓글" ||..o{ "댓글 좋아요" : "comment_id"

    "유저정보" {
        BIGINT id PK
        VARCHAR nickname "수의사는 이름으로"
        VARCHAR user_uuid
        VARCHAR type "보호자, 수의사"
    }
    "게시판" {
        BIGINT id PK
        VARCHAR name "NULL"
    }
    "카테고리" {
        BIGINT id PK
        VARCHAR name
    }
    "게시글" {
        BIGINT id PK
        BIGINT board_id
        BIGINT category_id
        BIGINT user_uuid
        VARCHAR title
        VARCHAR content
        INTEGER like_count "NULL"
        INTEGER view_count "NULL"
        INTEGER commnet_count "NULL"
        INTEGER alert_count
        DATETIME created_at
        DATETIME updated_at "NULL"
        DATETIME deleted_at "NULL"
    }
    "게시글 미디어" {
        BIGINT id PK
        BIGINT post_id
        VARCHAR(255) file_name "NULL"
        VARCHAR(10) media_type
        VARCHAR(45) file_extension
        INTEGER file_size
        VARCHAR(45) description
        VARCHAR(255) media_url
        DATETIME created_at
        DATETIME updated_at "NULL"
        DATETIME deleted_at "NULL"
    }
    "게시글 좋아요" {
        BIGINT id PK
        BIGINT post_id
        VARCHAR user_uuid
        VARCHAR role
        DATETIME created_at
    }
    "댓글" {
        BIGINT id PK
        BIGINT post_id
        BIGINT parent_comment_id "NULL"
        BIGINT user_uuid
        BIGINT sort_number
        BIGINT root_comment_id
        BIGINT depth
        VARCHAR content
        INTEGER state
        INTEGER like_count
        INTEGER alert_count
        DATETIME created_at
        DATETIME updated_at "NULL"
        DATETIME deleted_at "NULL"
        VARCHAR reason "NULL"
    }
    "댓글 좋아요" {
        BIGINT id PK
        BIGINT comment_id
        VARCHAR user_UUID
        VARCHAR role
        DATETIME created_at
    }
```

게시글과 댓글의 `user_uuid`는 `BIGINT`이고 `유저정보.user_uuid`와 좋아요 테이블의 사용자 UUID는 `VARCHAR`다. 작성자와 좋아요 사용자에 각각 어떤 식별자를 저장할지 확인해야 한다.

## 7. 관리자 · 신고

```mermaid
erDiagram
    "관리자" ||..o{ "관리자권한" : "admin_id"
    "권한" ||..o{ "관리자권한" : "role_id"
    "신고" ||..o{ "신고 사유 선정" : "report_id"
    "신고 사유" ||..o{ "신고 사유 선정" : "report_reason_id"

    "관리자" {
        BIGINT id PK
        VARCHAR(255) uuid "NULL"
        VARCHAR tel_no "NULL"
        VARCHAR email
        DATETIME created_at
        DATETIME updated_at
        DATETIME deleted_at "NULL"
    }
    "권한" {
        BIGINT id PK
        VARCHAR name
    }
    "관리자권한" {
        BIGINT id PK
        BIGINT admin_id
        BIGINT role_id
    }
    "신고" {
        BIGINT id PK
        VARCHAR uuid
        VARCHAR reporter_type "caregiver, veterinarian"
        VARCHAR target_uuid
        VARCHAR target_type "Enum (CAREGIVER, VETERINARIAN, BOARD, COMMENT)"
        VARCHAR content "신고자가 작성한 내용(자유양식)"
        VARCHAR status "Enum(RECEIVED, IN_PROGRESS, COMPLETED )"
        VARCHAR reviewer_user_id "NULL"
        VARCHAR resolution_note "NULL"
        DATETIME created_at
        DATETIME reviewed_at "NULL"
    }
    "신고 사유" {
        BIGINT id PK
        VARCHAR target_type
        VARCHAR code
        VARCHAR name
        BOOLEAN active "신고 사유 코드의 사용 여부"
    }
    "신고 사유 선정" {
        BIGINT id PK
        BIGINT report_id
        BIGINT report_reason_id
    }
```

`신고.target_uuid`는 `target_type`에 따라 참조 대상이 달라진다. 게시글과 댓글에는 첨부본 기준 `BIGINT id`가 있어 신고 대상 식별 방식과 `reviewer_user_id`의 참조 대상을 확인해야 한다.

## 참고

문서 구성은 [FinPlay 백엔드 ERD](https://github.com/finplay-team/finplay-backend/blob/dev/docs/erd.md)의 엔티티 목록과 도메인별 다이어그램 형식을 따랐다.
