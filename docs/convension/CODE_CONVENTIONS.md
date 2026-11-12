# 루이쿠리 코드 컨벤션

## 1. 적용 범위

### 1.1 적용 대상

- 백엔드 소스 코드와 테스트 코드에 적용한다. DB 마이그레이션, 빌드 설정, 프로젝트 스크립트에는 해당 파일을 다루는 규칙을 적용한다.
- 자동 생성 코드와 저장소에 포함된 외부 코드는 적용 대상에서 제외한다. 생성 결과를 바꿔야 하면 수정할 수 있는 원본이나 생성 설정에서 변경한다.

### 1.2 적용 시점

- 새로 추가하는 코드에는 관련 규칙을 모두 적용한다.
- 기존 코드에는 이번 변경에서 추가하거나 수정한 부분을 기준으로 적용한다. 파일 이름이나 import 순서처럼 파일 단위로 판단하는 규칙은 해당 변경과 관련된 범위까지 적용한다.
- 변경 범위를 벗어나는 기존 위반은 별도 변경으로 정리한다.

### 1.3 강제 수준

- **필수** 규칙에 명시된 기준을 지킨다.
- **금지** 규칙에 명시된 패턴을 사용하지 않는다.
- **권장** 규칙을 기본으로 따른다. 적용하기 어려우면 리뷰에서 이유를 설명할 수 있다.
- 필수·금지 규칙 위반은 머지 전에 수정하거나 아래 예외 기준에 따라 처리한다.

### 1.4 예외

- 외부 API 계약, 프레임워크 제약 또는 기존 호환성 때문에 필수·금지 규칙을 그대로 적용하기 어려울 때 예외를 검토한다.
- 예외는 필요한 범위에 한정한다. 적용할 수 없는 규칙, 사유, 적용 범위를 PR에 적고 리뷰에서 확인한다. 임시 예외라면 해소 조건도 적는다.

## 2. 파일과 코드 서식

아래 규칙은 필수로 적용한다. 코드 예시는 Java 문법으로 표기한다.

### 2.1 파일 형식

- 텍스트 소스 파일은 UTF-8(BOM 없음)로 저장하고, 줄바꿈은 LF를 사용한다.
- 비어 있지 않은 파일은 마지막 줄을 개행 하나로 끝낸다. 파일 끝에 빈 줄을 덧붙이지 않는다.
- 줄 끝의 불필요한 공백과 탭을 제거한다.

### 2.2 들여쓰기와 공백

- 블록이 한 단계 깊어질 때마다 스페이스 4칸으로 들여쓴다. 들여쓰기에 탭을 사용하지 않는다.
- 대입 및 이항 연산자 양옆과 쉼표 뒤에 공백을 한 칸 넣는다. 쉼표 앞과 소괄호 안쪽에는 공백을 넣지 않는다.
- `if`, `for`, `while`, `switch`, `catch` 같은 키워드와 여는 소괄호 사이에는 공백을 한 칸 넣는다. 메서드 이름과 여는 소괄호는 붙여 쓴다.
- 선언이나 대입의 열을 맞추기 위해 공백을 여러 칸 넣지 않는다.

**허용**

```java
if (petId != null) {
    int limit = pageSize + 1;
    return loadRecords(petId, limit);
}
```

**위반**

```java
if( petId!=null ) {
  int limit   = pageSize+1;
  return loadRecords (petId,limit);
}
```

### 2.3 줄 길이와 여러 줄 표현식

- 한 줄은 들여쓰기를 포함해 120자 이내로 작성한다. URL이나 외부 계약에서 정한 값처럼 줄을 나누면 읽기 어렵거나 의미가 달라지는 경우에는 해당 줄의 예외를 허용한다.
- 호출이나 선언의 인자 목록을 여러 줄로 나눌 때는 여는 소괄호 다음에서 줄을 바꾸고 인자를 한 줄에 하나씩 배치한다. 이어지는 줄은 스페이스 4칸을 추가하고, 닫는 소괄호는 표현식의 시작 줄과 같은 깊이에 둔다.
- 연쇄 호출을 여러 줄로 나눌 때는 메서드 호출을 한 줄에 하나씩 배치하고, 마침표를 이어지는 줄의 맨 앞에 둔다.

**허용**

```java
return consultationService.create(
    petId,
    veterinarianId,
    requestedAt,
    consultationReason
);
```

**위반**

```java
return consultationService.create(petId, veterinarianId,
                                  requestedAt, consultationReason);
```

### 2.4 중괄호와 빈 줄

- 여는 중괄호는 선언이나 제어문의 끝에 공백 한 칸을 두고 같은 줄에 쓴다. 닫는 중괄호는 블록을 연 줄과 같은 깊이에 둔다.
- 본문이 한 줄이어도 조건문과 반복문에는 중괄호를 쓴다. `else`, `catch`, `finally`는 앞 블록의 닫는 중괄호와 같은 줄에 둔다.
- 메서드와 메서드 사이에는 빈 줄을 한 줄 둔다. 메서드 안에서는 작업 단계가 바뀌는 지점에 빈 줄 한 줄로 구분할 수 있다. 빈 줄을 연속으로 두거나 블록의 첫 줄과 마지막 줄을 비워 두지 않는다.

**허용**

```java
if (record.isEmpty()) {
    return defaultRecord;
} else {
    return record.get();
}
```

**위반**

```java
if (record.isEmpty())
    return defaultRecord;
else
    return record.get();
```

### 2.5 import와 선언 순서

- 패키지 선언, import 목록, 타입 선언을 순서대로 두고 각 부분 사이에 빈 줄 한 줄을 둔다.
- import는 일반 import와 정적 import 순서로 그룹을 나눈다. 두 그룹 사이에 빈 줄 한 줄을 두고, 각 그룹 안에서는 전체 이름을 오름차순으로 정렬한다.
- 와일드카드 import는 사용하지 않는다. 사용하지 않는 import는 제거한다.
- 클래스 안에서는 상수, 필드, 생성자, 메서드, 중첩 타입 순서로 선언한다. 특정 메서드에서만 호출하는 private 메서드는 호출하는 메서드 가까이에 둘 수 있다.

**허용**

```java
import java.time.Instant;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
```

**위반**

```java
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import java.time.Instant;
```

## 3. 이름 짓기

### 3.1 서비스 디렉터리와 패키지

- 마이크로서비스 프로젝트 디렉터리 이름은 저장소 이름에 맞춰 영문 소문자와 하이픈으로 작성하고, 끝에 `-service`를 붙인다. 예를 들어 `product-service/`, `medical-record-service/`로 쓴다.
- Java 루트 패키지의 서비스명은 여러 단어여도 소문자로 붙여 쓴다. 예를 들어 `com.louiekury.product`, `com.louiekury.medicalrecord`로 쓴다.

### 3.2 요청·응답 DTO

- 요청·응답 DTO는 일반 `class`로 선언하고, 이름 끝에 `Dto`를 붙인다.
- 요청 DTO는 동작, 대상, `RequestDto` 순으로 이름을 짓는다. 예를 들어 `CreateProductRequestDto`, `UpdateProductRequestDto`로 쓴다.
- 응답 DTO 이름은 응답이 담는 대상을 드러내고 `ResponseDto`로 끝낸다. 예를 들어 `ProductResponseDto`로 쓴다.
- 목록에서 한 항목을 담는 DTO는 `ListItemResponseDto`로 끝낸다. 예를 들어 상품 목록의 각 항목은 `ProductListItemResponseDto`로 표현한다.

### 3.3 조회 메서드

- Spring Data 레포지토리의 조회와 존재 확인은 각각 `findById()`, `existsById()` 같은 기존 이름을 따른다.
- 서비스에서 조회 결과가 반드시 필요할 때는 `getProduct()`처럼 `get`으로 시작하는 이름을 쓰고, 결과가 없으면 예외를 던진다.

### 3.4 도메인 용어와 약어

- 도메인 용어는 뜻을 명확하게 알 수 있도록 풀어 쓴다. 예를 들어 수의사를 나타내는 이름에는 `veterinarian`을 사용한다.
- 같은 개념은 관련 클래스, 메서드, 변수에서 같은 용어로 표현한다. 예를 들어 `VeterinarianResponseDto`, `findVeterinarian()`, `veterinarianId`로 쓴다.
- `API`, `ID`, `URL`, `DTO` 같은 약어는 이름을 구성할 때 한 단어로 취급하고, 이름 전체의 대소문자 표기법을 따른다. 예를 들어 `ProductApiClient`, `productId`, `imageUrl`, `ProductResponseDto`로 쓴다.

### 3.5 테스트 이름

- 테스트 메서드 이름은 검증하는 동작이 드러나게 영어로 작성하고, `@DisplayName`에는 테스트 조건과 기대 결과가 드러나는 한글 설명을 작성한다.

```java
@Test
@DisplayName("이미 등록된 상품명으로 등록하면 실패한다")
void rejectsDuplicateProductName() {
    // 테스트 본문
}
```

### 3.6 타입과 파일 이름

- 클래스, 인터페이스, 열거형은 각 단어의 첫 글자를 대문자로 쓰는 `PascalCase`를 사용한다. 공개 타입을 선언한 Java 파일은 타입과 같은 이름을 사용한다.
- Java `record` 타입 사용은 금지한다.
- 컨트롤러, 서비스, 레포지토리에는 대상 뒤에 역할을 붙인다. 예를 들어 `ProductController`, `ProductService`, `ProductRepository`로 쓴다.
- 엔티티는 도메인 용어로 이름을 짓고 `Entity`를 붙이지 않는다. 예를 들어 상품 엔티티는 `entity/Product.java`에 둔다.

### 3.7 정적 팩토리 메서드 이름

- 기존 객체 하나를 받아 변환할 때는 `from`을 쓴다. 예를 들어 `ProductResponseDto.from(product)`로 쓴다.
- DTO를 만들 때 필요한 필드 값을 직접 전달하는 팩토리 메서드는 `of`로 이름을 짓는다. 예를 들어 `CreateProductRequestDto.of(name, price)`로 쓴다.

### 3.8 메서드, 변수, 상수

- 메서드, 필드, 지역 변수, 매개변수는 `lowerCamelCase`로 쓴다. 메서드는 `updateProductName()`처럼 동작을 드러내고, 변수는 `productName`처럼 담긴 값을 드러낸다.
- 상수는 단어를 밑줄로 구분한 대문자(`UPPER_SNAKE_CASE`)로 쓴다. 예를 들어 `MAX_RETRY_COUNT`로 쓴다.
- 숫자 타입에 단위가 드러나지 않으면 이름에 단위를 적는다. 예를 들어 밀리초를 담는 변수는 `timeoutMillis`로 쓴다.
- 참·거짓을 나타내는 필드는 `active`처럼 상태 이름으로 짓고, 기본형 `boolean`의 getter에는 `is`를 붙인다. 예를 들어 `boolean active`의 getter는 `isActive()`로 쓴다.

### 3.9 업무 예외와 오류 코드

- 업무 규칙에 따른 실패는 공통 예외인 `BusinessException`으로 표현하고, 구체적인 실패 사유를 오류 코드로 구분한다.
- 오류 코드는 대상과 실패 사유가 드러나도록 `UPPER_SNAKE_CASE`로 쓴다. 예를 들어 상품을 찾을 수 없으면 `PRODUCT_NOT_FOUND`를 사용한다.

```java
throw new BusinessException(ErrorCode.PRODUCT_NOT_FOUND);
```

## 4. 패키지와 계층 구조

### 4.1 서비스별 기본 패키지

각 마이크로서비스의 루트 패키지는 `com.louiekury.<서비스명>`으로 구성하고, 실행 클래스는 루트 패키지에 둔다. 루트 아래에 `controller`, `service`, `repository`, `entity`, `dto`를 두고, API 요청과 응답 DTO는 각각 `dto.request`와 `dto.response`에 둔다. 서비스 전역에서 쓰는 코드는 `global`에 둔다.

상담 서비스의 예시는 다음과 같다.

```text
consultation-service/
└── src/main/java/com/louiekury/consultation/
    ├── ConsultationApplication.java
    ├── controller/
    ├── service/
    ├── repository/
    ├── entity/
    │   └── Consultation.java
    ├── dto/
    │   ├── request/
    │   │   └── CreateConsultationRequestDto.java
    │   └── response/
    │       └── ConsultationResponseDto.java
    └── global/
        ├── config/
        └── exception/
```

| 패키지 | 배치할 코드 |
| --- | --- |
| `controller` | HTTP 요청을 받고 응답을 만드는 코드 |
| `service` | 상담 요청·취소·완료처럼 유스케이스의 처리 흐름을 담당하는 코드 |
| `repository` | 서비스가 소유한 데이터의 조회와 저장을 담당하는 코드 |
| `entity` | `Consultation`처럼 서비스가 저장하고 관리하는 엔티티 |
| `dto.request` | `CreateConsultationRequestDto` 같은 API 요청 DTO |
| `dto.response` | `ConsultationResponseDto` 같은 API 응답 DTO |
| `global` | 서비스 전역의 설정과 공통 예외 응답 처리 |

별도 서비스가 책임지는 기능과 데이터는 해당 서비스에 둔다. 하나의 서비스 안에서 기능이 커져 관련 코드의 위치를 구분할 필요가 생기면 기능별 하위 패키지를 둘 수 있다.

### 4.2 응답 DTO 변환

- 서비스는 레포지토리에서 필요한 데이터를 받아 비즈니스 로직을 수행한다. 처리 결과로 응답 DTO를 만들 때는 DTO의 정적 팩토리 메서드를 호출한다.
- 팩토리 메서드는 변환한 DTO를 서비스에 반환하고, 서비스는 그 DTO를 컨트롤러에 반환한다.
- 컨트롤러는 서비스가 반환한 DTO를 공통 응답에 담고, `ResponseEntity`로 HTTP 상태와 응답 본문을 함께 반환한다. 서비스 호출 결과를 공통 응답에 한 번만 담을 때는 반환문에서 바로 호출한다.

조회 서비스 코드는 [상품 등록 및 조회 예시](#53-상품-등록-및-조회-예시)를 참고한다.

### 4.3 요청 DTO 전달과 변환

- 컨트롤러는 요청 DTO를 서비스 메서드의 인자로 그대로 전달한다.
- 서비스는 요청 DTO에서 유스케이스에 필요한 값을 읽는다. 엔티티를 만들 때는 필요한 값을 생성자에 전달한다.

등록 컨트롤러와 서비스 코드는 [상품 등록 및 조회 예시](#53-상품-등록-및-조회-예시)를 참고한다.

### 4.4 서비스와 레포지토리의 의존 방향

- 각 서비스 클래스는 자신이 담당하는 기능의 레포지토리를 사용한다. 다른 기능의 레포지토리를 직접 주입하거나 호출하는 것은 금지한다.
- 같은 마이크로서비스에서 다른 기능의 데이터나 처리가 필요하면 그 기능을 담당하는 서비스의 공개 메서드를 호출한다. 서비스 클래스 간 호출은 한 방향으로 유지하며 순환 의존은 금지한다.
- 별도 마이크로서비스가 소유한 데이터는 해당 서비스가 공개한 API나 이벤트를 통해 받는다.

예를 들어 상품과 재고가 같은 마이크로서비스에 있으면 `ProductService`는 `stockService.getQuantity(productId)`를 호출한다. `StockService`가 `StockRepository`에서 재고를 조회해 수량을 반환하고, `ProductService`는 받은 수량으로 상품 응답을 구성한다.

### 4.5 공개 메서드와 반환값

- 다른 클래스가 호출해야 하는 메서드만 공개한다. 클래스 내부에서만 사용하는 보조 메서드는 `private`으로 선언한다.
- 다른 기능에 공개하는 서비스 메서드는 호출에 필요한 값만 반환한다. 값 하나면 해당 값의 타입으로 반환하고, 관련 값 여러 개를 전달해야 하면 필요한 필드만 담은 DTO를 반환한다.
- 예를 들어 `StockService.getQuantity(productId)`는 재고 수량을 반환한다. 상품 기능에서 쓰는 공개 메서드의 반환 타입은 필요한 값인 수량을 나타낸다.

## 5. 클래스와 메서드

### 5.1 객체 생성과 변환

- 애플리케이션 코드에서 DTO를 만들 때는 반드시 정적 팩토리 메서드 `from` 또는 `of`를 호출한다.
- DTO의 필드 매핑과 객체 생성은 팩토리 메서드에서 처리한다. DTO 빌더는 팩토리 내부에서 사용하도록 `@Builder(access = AccessLevel.PRIVATE)`로 선언한다. 엔티티는 값을 받는 생성자로 초기화한다. 상태 변경이 필요한 필드에는 해당 변경 메서드만 공개한다.
- HTTP 요청 본문을 역직렬화할 때 Jackson은 요청 DTO의 `@JsonCreator`가 붙은 정적 팩토리 메서드를 호출한다. 서비스는 전달받은 DTO에서 엔티티 생성에 필요한 값을 읽는다.

### 5.2 계층별 어노테이션

| 대상 | 기본 사용 | 필요한 경우 |
| --- | --- | --- |
| 컨트롤러 | 클래스에 `@RestController`와 공통 경로를 지정하는 `@RequestMapping`을 붙인다. 엔드포인트에는 `@GetMapping`, `@PostMapping` 등 HTTP 메서드에 맞는 매핑을 하나 붙인다. | 본문 DTO에는 `@Valid @RequestBody`, 경로 변수에는 `@PathVariable`을 붙인다. HTTP 상태와 공통 응답 본문은 `ResponseEntity`에서 지정한다. |
| 서비스 | 클래스에 `@Service`를 붙인다. | DB 쓰기 유스케이스의 공개 메서드에는 `@Transactional`, DB 조회 전용 유스케이스에는 `@Transactional(readOnly = true)`를 붙인다. |
| 레포지토리 | Spring Data JPA 인터페이스는 `JpaRepository<엔티티, ID 타입>`를 상속한다. 인터페이스에 `@Repository`를 중복 선언하지 않는다. | 복잡한 조회는 [조회 방식 선택](#92-조회-방식-선택) 기준에 따라 Querydsl로 작성한다. |
| 요청 DTO | `private final` 필드, `@Getter`, `@RequiredArgsConstructor(access = AccessLevel.PRIVATE)`를 사용한다. `of`와 비공개 빌더로 생성한다. | JSON 본문과 연결하는 `of`에 `@JsonCreator`, 매개변수에 `@JsonProperty`를 붙인다. 입력 제약은 필드 위에 하나씩 한 줄에 쓴다. 각 필드와 그 어노테이션을 한 묶음으로 두고, 묶음 사이에 빈 줄을 한 줄 둔다. |
| 응답 DTO | 클래스로 선언하고, 필드는 `private final`로 둔다. `@Getter`로 조회 메서드를 만들고, `@RequiredArgsConstructor(access = AccessLevel.PRIVATE)`로 생성자를 만든다. | 단일 엔티티를 변환할 때는 `from`과 비공개 빌더를 쓴다. |
| 엔티티 | 클래스 어노테이션은 `@Getter`, `@Entity`, `@Table(name = "...")`, `@NoArgsConstructor` 순서로 붙인다. `@Table`에 테이블 이름을 명시하고 식별자 필드에 `@Id`를 붙인다. JPA용 기본 생성자는 `@NoArgsConstructor(access = AccessLevel.PROTECTED)`로 만들고, 값을 초기화하는 생성자는 직접 작성한다. | JPA가 생성하는 식별자에는 `@GeneratedValue(strategy = ...)`로 스키마에 맞는 생성 전략을 명시한다. 컬럼 제약, 연관관계, 읽기 접근자는 필요한 곳에 선언한다. |

- 클래스의 필드는 특별한 이유가 있으면 접근 범위를 넓힐 수 있으며, 기본은 `private`으로 선언한다.
- 컨트롤러와 서비스의 의존성은 `private final` 필드와 `@RequiredArgsConstructor`로 주입한다. 필드에 `@Autowired`를 붙이는 방식은 금지한다.
- DTO의 `final`은 필드에만 붙인다.
- DTO와 엔티티에서 `@Data`와 클래스 전체에 적용하는 `@Setter`는 금지한다.

### 5.3 상품 등록 및 조회 예시

#### 5.3.1 컨트롤러 · ProductController.java

이 예시에서는 공통 성공 응답 타입을 `ApiResponseDto<T>`로 표기한다.

```java
package com.louiekury.product.controller;

import com.louiekury.product.dto.request.CreateProductRequestDto;
import com.louiekury.product.dto.response.ProductResponseDto;
import com.louiekury.product.global.response.ApiResponseDto;
import com.louiekury.product.service.ProductService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;

    @PostMapping
    public ResponseEntity<ApiResponseDto<ProductResponseDto>> createProduct(
        @Valid @RequestBody CreateProductRequestDto request
    ) {
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(ApiResponseDto.of(productService.createProduct(request)));
    }

    @GetMapping("/{productId}")
    public ResponseEntity<ApiResponseDto<ProductResponseDto>> getProduct(
        @PathVariable("productId") Long productId
    ) {
        return ResponseEntity.ok(ApiResponseDto.of(productService.getProduct(productId)));
    }
}
```

#### 5.3.2 서비스 · ProductService.java

```java
package com.louiekury.product.service;

import com.louiekury.product.dto.request.CreateProductRequestDto;
import com.louiekury.product.dto.response.ProductResponseDto;
import com.louiekury.product.entity.Product;
import com.louiekury.product.global.exception.BusinessException;
import com.louiekury.product.global.exception.ErrorCode;
import com.louiekury.product.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;

    @Transactional
    public ProductResponseDto createProduct(CreateProductRequestDto request) {
        Product product = new Product(request.getName(), request.getPrice());
        Product savedProduct = productRepository.save(product);
        return ProductResponseDto.from(savedProduct);
    }

    @Transactional(readOnly = true)
    public ProductResponseDto getProduct(Long productId) {
        Product product = productRepository.findById(productId)
            .orElseThrow(() -> new BusinessException(ErrorCode.PRODUCT_NOT_FOUND));
        return ProductResponseDto.from(product);
    }
}
```

#### 5.3.3 레포지토리 · ProductRepository.java

```java
package com.louiekury.product.repository;

import com.louiekury.product.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<Product, Long> {
}
```

#### 5.3.4 요청 DTO · CreateProductRequestDto.java

```java
package com.louiekury.product.dto.request;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import java.math.BigDecimal;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor(access = AccessLevel.PRIVATE)
@Builder(access = AccessLevel.PRIVATE)
public class CreateProductRequestDto {

    @NotBlank
    private final String name;

    @NotNull
    @Positive
    private final BigDecimal price;

    @JsonCreator
    public static CreateProductRequestDto of(
        @JsonProperty("name") String name,
        @JsonProperty("price") BigDecimal price
    ) {
        return CreateProductRequestDto.builder()
            .name(name)
            .price(price)
            .build();
    }
}
```

#### 5.3.5 응답 DTO · ProductResponseDto.java

```java
package com.louiekury.product.dto.response;

import com.louiekury.product.entity.Product;
import java.math.BigDecimal;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor(access = AccessLevel.PRIVATE)
@Builder(access = AccessLevel.PRIVATE)
public class ProductResponseDto {

    private final Long id;
    private final String name;
    private final BigDecimal price;

    public static ProductResponseDto from(Product product) {
        return ProductResponseDto.builder()
            .id(product.getId())
            .name(product.getName())
            .price(product.getPrice())
            .build();
    }
}
```

#### 5.3.6 엔티티 · Product.java

```java
package com.louiekury.product.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@Entity
@Table(name = "products")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private BigDecimal price;

    public Product(String name, BigDecimal price) {
        this.name = name;
        this.price = price;
    }
}
```

### 5.4 추가로 정할 항목

- 클래스의 책임과 분리 기준
- 매개변수 개수, 분기 복잡도
- 상태 변경, 불변성, 부수 효과
- 조건문, 반복문, 조기 반환, 중복 코드
- 널, 빈 값, 컬렉션 반환값

## 6. 도메인 로직

- 객체 생성과 유효성 검증 위치
- 비즈니스 제약과 상태 전이
- 식별자, 값 객체, 열거형의 사용 범위
- 시간대, 날짜·시간, 수량·금액 계산

## 7. API와 데이터 계약

- 리소스 경로, HTTP 메서드, 상태 코드
- 요청·응답 필드 이름, 타입, 필수 여부
- 입력 검증, 직렬화, 날짜·시간 표현
- 목록의 페이지네이션, 정렬, 필터링
- 응답 스키마, 버전, 호환성, API 명세 동기화

## 8. 예외와 오류 응답

- 입력 오류, 도메인 오류, 인프라 오류 구분
- 예외의 생성·변환·처리 위치
- 오류 코드, 메시지, 응답 형식
- 실패 전파, 재시도, 복구와 오류 로그

## 9. 데이터베이스와 트랜잭션

### 9.1 엔티티 연관관계와 ID 참조

| 상황 | 구현 기준 | 예시 |
| --- | --- | --- |
| 같은 마이크로서비스가 두 데이터를 소유하고, 업무 로직에서 여러 행이 참조하는 상위 엔티티를 객체로 다뤄야 한다. | `@ManyToOne`으로 연관관계를 매핑한다. | 상품 이미지 여러 장이 하나의 상품에 속하고, 이미지 등록에서 상품 상태를 검사한다. |
| 같은 마이크로서비스 안에서 상대 객체를 탐색할 필요가 없고, 식별자만으로 업무를 처리할 수 있다. | ID 필드를 사용한다. 같은 DB에서 참조 무결성이 필요하면 외래 키로 보장할 수 있다. | 상품 조회 기록을 상품 ID로 집계한다. |
| 대상 데이터를 별도 마이크로서비스가 소유한다. | 외부 서비스의 ID를 저장하고, 필요한 데이터는 그 서비스의 API나 이벤트로 받는다. | 주문 서비스의 주문 항목에 상품 서비스의 `productId`를 저장한다. |

**연관관계 예시 · 상품 이미지 엔티티**

```java
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "product_id", nullable = false)
private Product product;
```

**ID 참조 예시 · 주문 항목 엔티티**

```java
@Column(name = "product_id", nullable = false)
private Long productId;
```

연관관계를 매핑했다면 지연 로딩을 기본으로 명시하고, 연관 데이터가 필요한 조회에서 가져올 범위를 정한다. ID 참조도 목록의 각 ID를 개별 조회하면 호출이 늘어난다. 목록은 필요한 데이터를 묶어서 조회하고, 실제 SQL이나 API 호출 횟수를 확인한다. [Hibernate ORM 조회 전략](https://docs.hibernate.org/orm/7.1/userguide/html_single/#fetching), [마이크로서비스 데이터 소유권](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/data-considerations)

### 9.2 조회 방식 선택

- 기본 CRUD와 단순 조회는 `JpaRepository`의 기본 메서드와 메서드 이름으로 쿼리를 생성하는 방식을 사용한다.
- 선택 조건을 여러 개 조합하거나 조인·집계로 쿼리가 복잡해지는 조회는 Querydsl로 작성한다. 예를 들어 상담 목록에서 상태·수의사·기간 중 전달받은 조건만 조합해 조회한다.
- 실행 성능을 개선하려고 조회 방식을 바꾸는 경우에는 실제 SQL, 쿼리 횟수, 필요에 따라 실행 계획을 비교한다.

### 9.3 추가로 정할 항목

- `BaseEntity`에 둘 공통 필드와 상속을 적용할 엔티티의 범위
- 테이블, 컬럼, 키, 인덱스 이름
- 스키마 제약, 마이그레이션 파일과 변경 절차
- 쿼리 작성 위치, 조회 범위, 성능 확인
- 트랜잭션 시작과 종료, 실패 시 롤백
- 동시성, 중복 요청, 데이터 정합성

## 10. 외부 연동과 비동기 처리

- 외부 클라이언트와 연동 모델의 위치
- 시간 제한, 재시도, 장애 시 처리
- 이벤트 이름과 데이터 형식
- 중복 처리, 순서, 멱등성

## 11. 보안과 설정

- 인증·인가 검사 위치와 권한 검증
- 외부 입력 검증과 민감정보 처리
- 환경 변수, 비밀값, 설정 파일 이름
- 환경별 설정 분리와 누락된 설정 처리

## 12. 로깅과 모니터링

- 로그 수준, 메시지 형식, 공통 필드
- 요청·작업 추적 식별자
- 민감정보 마스킹과 로그 제외 항목
- 메트릭, 상태 확인, 장애 진단 정보

## 13. 테스트 코드

- 테스트 파일 위치, 이름, 시나리오 표현
- 단위·통합·API 테스트의 범위
- 픽스처, 테스트 데이터, 테스트 간 격리
- Mock과 실제 의존성을 사용하는 범위
- 정상·경계·실패·회귀 사례와 검증 방식

## 14. 주석과 코드 문서

- 주석을 작성하는 경우와 설명 범위
- 공개 API 문서와 사용 예시
- TODO·FIXME 표기와 추적 방법

## 15. 자동 검사와 코드 리뷰

- 포매터, 린터, 정적 분석의 설정과 실행 위치
- CI 검사 항목과 실패 처리
- 리뷰에서 확인할 항목과 예외 기록
- 규칙 변경과 기존 코드 정리 절차

## 규칙별 작성 양식

```markdown
#### 규칙 이름

- 적용 대상
- 강제 수준
- 구체적인 기준
- 적용 이유
- 허용 예시
- 위반 예시
- 예외 조건
- 확인 방법
```
