import streamlit as st
import random as rd
import sympy

def gen_string(a, b):
    return f"({str(a)}{rd.choice(['+', '-'])}{str(b)})"

def gen_question():
    res = ""
    l = [str(j) for j in range(2, 6)]
    num = rd.randint(3, max_n)
    res += rd.choice([""]*70+["-"]*30)
    i = 0
    while i < num:
        #0. xとn 1. yとn 2. xとy 3. x^2とxとn
        if (tmp := rd.randint(0, 0 if not (include_y or include_x2) else 1 if not include_y else 2 if i-num == 1 or not include_x2 else 3)) == 0:
            if rd.randint(0, 1) == 0:
                res += gen_string("x", rd.randint(1, 10))
            else:
                res += gen_string(f'{rd.choice(l)}*x', rd.randint(1, 10))
        elif tmp == 1 and include_y:
            if rd.randint(0, 1) == 0:
                res += gen_string("y", rd.randint(1, 10))
            else:
                res += gen_string(f'{rd.choice(l)}*y', rd.randint(1, 10))
        elif tmp == 2 and include_y:
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
        elif tmp == 3 or (tmp == 1 and include_x2 and not include_y):
            if rd.randint(0, 1) == 0:
                res += f'(x**2{rd.choice(["+", "-"])+str(rd.randint(1, 10))}*x{rd.choice(["+", "-"])+str(rd.randint(1, 10))})'
            else:
                res += f'({rd.choice(l)}*x**2{rd.choice(["+", "-"])+rd.choice(l)}*x{rd.choice(["+", "-"])+str(rd.randint(1, 10))})'
            num-=1
        if i+1 != num: res += r"*"
        i += 1
    return res[:-1] if res.endswith("*") else res #なんかおかしいから対策

def reshape(s):
    res = str(s).replace(" ", "")
    for j in range(2, 10):
        res = res.replace(r"**"+str(j), unilis[j-2])
    return res.replace(r"*", "")

unilis = list(map(lambda x: eval(r'b"\\u'+x.replace("U+", "")+'"').decode("unicode-escape"), ["U+00B2", "U+00B3", "U+2074", "U+2075", "U+2076", "U+2077", "U+2078", "U+2079"]))
sympy.var('x y z')
anslis = []
st.title("因数分解ガチャ(パクリ)")
st.subheader("下記の式を整数係数の範囲で因数分解してください。")
if hell := st.checkbox("✟ヘルモード✟"):
    include_x2 = True
    include_y = True
    max_n = rd.randint(7, 9)
else:
    if include_y := st.checkbox("yを含む式を出題する"): pass
    if include_x2 := st.checkbox("分解後にx^2を含む式を出題する"): pass
    if max_n := st.selectbox("項数の最大値", range(3, 8)): pass
for i in range(1, 6):
    a = gen_question()
    anslis.append(f"({i}) "+reshape(sympy.factor(a)))
    st.text(f"({i}) {reshape(sympy.expand(a))}")
with st.expander("解答を見る"):
    for c in anslis:
        st.text(c)
st.text("\n\n")
st.button("もう一度回す")
