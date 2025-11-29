import math
import numpy as np
import plotly.graph_objs as go
import streamlit as st


def main():
    # 페이지 기본 설정
    st.set_page_config(
        page_title="다기능 수학 계산기",
        page_icon="🧮",
        layout="centered",
    )

    st.title("🧮 다기능 수학 계산기")
    st.write("사칙연산, 모듈러, 지수, 로그 계산과 간단한 다항함수 그래프를 그릴 수 있는 웹앱입니다.")

    st.divider()

    tab_calc, tab_poly = st.tabs(["🔢 계산기", "📈 다항함수 그래프"])

    with tab_calc:
        calculator_ui()

    with tab_poly:
        polynomial_plot_ui()


# ---------------- 계산기 UI ---------------- #
def calculator_ui():
    st.subheader("🔢 기본 계산기")

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
        key="operation_select",
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
        a = st.number_input(label_a, value=0.0, help=help_a, key="a_input")
    with col2:
        b = st.number_input(label_b, value=0.0, help=help_b, key="b_input")

    st.write("")  # 여백
    calc_btn = st.button("계산하기", key="calc_button")

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


# ---------------- 다항함수 그래프 UI ---------------- #
def polynomial_plot_ui():
    st.subheader("📈 다항함수 그래프")

    st.write("계수를 입력해서 간단한 다항함수 \( f(x) \) 의 그래프를 그려봅니다.")
    degree = st.selectbox("다항식의 차수를 선택하세요.", [1, 2, 3], index=1, key="degree_select")

    st.markdown("#### 계수 입력 (f(x) = aₙxⁿ + ... + a₁x + a₀)")

    coeffs = []
    for i in range(degree, -1, -1):
        default = 1.0 if i == degree else 0.0
        coeff = st.number_input(
            f"x^{i} 의 계수 a{i}",
            value=default,
            key=f"coeff_{i}",
        )
        coeffs.append(coeff)

    st.markdown("#### x 구간 설정")
    col_min, col_max = st.columns(2)
    with col_min:
        x_min = st.number_input("x 최소값", value=-10.0, key="x_min")
    with col_max:
        x_max = st.number_input("x 최대값", value=10.0, key="x_max")

    plot_btn = st.button("그래프 그리기", key="plot_button")

    if plot_btn:
        if x_min >= x_max:
            st.error("x 최소값은 x 최대값보다 작아야 합니다.")
            return

        # x, y 값 계산
        x = np.linspace(x_min, x_max, 400)
        y = np.polyval(coeffs, x)

        expr = build_polynomial_expr(coeffs)

        st.markdown(f"**함수식:**  \n\( f(x) = {expr} \)")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="f(x)"))

        # 축 설정 (x=0, y=0 축을 눈금선으로 표시)
        fig.update_layout(
            xaxis=dict(title="x", zeroline=True, zerolinewidth=2),
            yaxis=dict(title="f(x)", zeroline=True, zerolinewidth=2),
            margin=dict(l=40, r=20, t=40, b=40),
        )

        st.plotly_chart(fig, use_container_width=True)


def build_polynomial_expr(coeffs):
    """
    coeffs: [a_n, a_{n-1}, ..., a_0]
    를 받아 사람이 읽기 쉬운 다항식 문자열로 변환.
    """
    degree = len(coeffs) - 1
    terms = []

    for idx, a in enumerate(coeffs):
        power = degree - idx
        if abs(a) < 1e-12:
            continue  # 0 계수는 생략

        # 계수 부분
        if power == 0:
            coeff_str = f"{a:g}"
        else:
            if a == 1:
                coeff_str = ""
            elif a == -1:
                coeff_str = "-"
            else:
                coeff_str = f"{a:g}"

        # x와 지수 부분
        if power == 0:
            term = f"{coeff_str}"
        elif power == 1:
            term = f"{coeff_str}x"
        else:
            term = f"{coeff_str}x^{power}"

        terms.append(term)

    if not terms:
        return "0"

    expr = terms[0]
    for term in terms[1:]:
        if term.startswith("-"):
            expr += f" - {term[1:]}"
        else:
            expr += f" + {term}"

    return expr


if __name__ == "__main__":
    main()
