import streamlit as st
import random as rd
import sympy

def gen_string(a, b):
    return f"({str(a)}{rd.choice(['+', '-'])}{str(b)})"

def gen_question():
    res = ""
    l = [str(j) for j in range(2, 6)]
    num = rd.randint(3, 6)
    res += rd.choice([""]*70+["-"]*30)
    i = 0
    while i < num:
        if (tmp := rd.randint(0, 3)) == 0:
            if rd.randint(0, 1) == 0:
                res += gen_string("x", rd.randint(1, 10))
            else:
                res += gen_string(f'{rd.choice(l)}*x', rd.randint(1, 10))
        elif tmp == 1:
            if rd.randint(0, 1) == 0:
                res += gen_string("y", rd.randint(1, 10))
            else:
                res += gen_string(f'{rd.choice(l)}*y', rd.randint(1, 10))
        elif tmp == 2:
            if rd.randint(0, 1) == 0:
                if rd.randint(0, 1) == 0:
                    res += gen_string("x", "y")
                else:
                    res += gen_string("x", f"{rd.choice(l)}*y")
            else:
                if rd.randint(0, 1) == 0:
                    res += gen_string(f'{rd.choice(l)}*x', "y")
                else:
                    res += gen_string(f'{rd.choice(l)}*x', f"{rd.choice(l)}*y")
        elif tmp == 3:
            if rd.randint(0, 1) == 0:
                res += f'(x**2{rd.choice(["+", "-"])+str(rd.randint(1, 10))}*x{rd.choice(["+", "-"])+str(rd.randint(1, 10))})'
            else:
                res += f'({rd.choice(l)}*x**2{rd.choice(["+", "-"])+rd.choice(l)}*x{rd.choice(["+", "-"])+str(rd.randint(1, 10))})'
        if i+1 != num: res += r"*"
        i += 1
    return res
def reshape(s):
    res = str(s).replace(" ", "")
    for j in range(2, 10):
        res = res.replace(r"**"+str(j), unilis[j-2])
    return res.replace(r"*", "")
unilis = list(map(lambda x: eval(r'b"\\u'+x.replace("U+", "")+'"').decode("unicode-escape"), ["U+00B2", "U+00B3", "U+2074", "U+2075", "U+2076", "U+2077", "U+2078", "U+2079"]))
sympy.var('x y z')
anslis = []
st.title("因数分解ガチャ")
st.subheader("下記の式を整数係数の範囲で因数分解してください。")
for i in range(1, 6):
    a = gen_question()
    anslis.append(f"({i}) "+reshape(sympy.factor(a)))
    q = reshape(sympy.expand(a))
    st.text(f"({i}) {q}")
with st.expander("解答を見る"):
    for c in anslis:
        st.text(c)
st.text("\n\n")
st.button("もう一度回す")