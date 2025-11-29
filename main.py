import math
import streamlit as st


def main():
    # 페이지 기본 설정
    st.set_page_config(
        page_title="다기능 수학 계산기",
        page_icon="🧮",
        layout="centered",
    )

    st.title("🧮 다기능 수학 계산기")
    st.write("사칙연산, 모듈러 연산, 지수 연산, 로그 연산을 지원하는 간단한 웹 계산기입니다.")

    st.divider()

    # 연산 선택
    operation = st.selectbox(
        "원하는 연산을 선택하세요.",
        (
            "덧셈 (a + b)",
            "뺄셈 (a - b)",
            "곱셈 (a × b)",
            "나눗셈 (a ÷ b)",
            "모듈러 (a mod b)",
            "지수 (a^b)",
            "로그 (log_b(a))",
        ),
    )

    # 선택된 연산에 따라 입력 레이블 설정
    if operation == "로그 (log_b(a))":
        label_a = "진수 a (a > 0)"
        label_b = "밑 b (b > 0, b ≠ 1)"
        help_a = "로그의 대상이 되는 값 a입니다. a는 0보다 커야 합니다."
        help_b = "로그의 밑 b입니다. b는 0보다 크고, 1이 될 수 없습니다."
    elif operation == "모듈러 (a mod b)":
        label_a = "피제수 a (정수)"
        label_b = "제수 b (정수, 0이 아님)"
        help_a = "나누어지는 수 a입니다. 정수로 취급합니다."
        help_b = "나누는 수 b입니다. 정수로 취급하며 0이 될 수 없습니다."
    else:
        label_a = "첫 번째 값 a"
        label_b = "두 번째 값 b"
        help_a = None
        help_b = None

    # 입력 영역
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input(label_a, value=0.0, help=help_a)
    with col2:
        b = st.number_input(label_b, value=0.0, help=help_b)

    st.write("")  # 약간의 여백
    calc_btn = st.button("계산하기")

    if calc_btn:
        try:
            result, expr = calculate(a, b, operation)
            if result is not None:
                st.success(f"결과: {expr} = **{result}**")
        except Exception as e:
            st.error(f"계산 중 오류가 발생했습니다: {e}")


def calculate(a: float, b: float, operation: str):
    """
    선택된 연산에 따라 a, b를 계산하고
    (결과, 표현식 문자열)을 반환합니다.
    """
    # 덧셈
    if operation == "덧셈 (a + b)":
        result = a + b
        expr = f"{a} + {b}"

    # 뺄셈
    elif operation == "뺄셈 (a - b)":
        result = a - b
        expr = f"{a} - {b}"

    # 곱셈
    elif operation == "곱셈 (a × b)":
        result = a * b
        expr = f"{a} × {b}"

    # 나눗셈
    elif operation == "나눗셈 (a ÷ b)":
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다.")
        result = a / b
        expr = f"{a} ÷ {b}"

    # 모듈러 연산
    elif operation == "모듈러 (a mod b)":
        int_a = int(a)
        int_b = int(b)
        if int_b == 0:
            raise ValueError("모듈러 연산에서 b는 0이 될 수 없습니다.")
        result = int_a % int_b
        expr = f"{int_a} mod {int_b}"

    # 지수 연산
    elif operation == "지수 (a^b)":
        result = a ** b
        expr = f"{a}^{b}"

    # 로그 연산 (log_b(a))
    elif operation == "로그 (log_b(a))":
        if a <= 0:
            raise ValueError("로그의 진수 a는 0보다 커야 합니다.")
        if b <= 0 or b == 1:
            raise ValueError("로그의 밑 b는 0보다 크고 1이 될 수 없습니다.")
        result = math.log(a, b)
        expr = f"log_{b}({a})"

    else:
        raise ValueError("알 수 없는 연산입니다.")

    return result, expr


if __name__ == "__main__":
    main()
