import streamlit as st
import secrets
import random
from sympy import symbols, Integer
import time

# Fungsi untuk membangkitkan kunci rahasia
def generate_secret_key():
    secret_key = secrets.token_hex(16)
    return secret_key

# Fungsi untuk membagi rahasia menggunakan Shamir's Secret Sharing
def split_secret(secret, n, k):
    coefficients = [secret] + [random.randrange(1, 256) for _ in range(k - 1)]  # Koefisien polinomial
    x = symbols('x')
    polynomial = sum(coeff * x**i for i, coeff in enumerate(coefficients))
    shares = [(i, polynomial.subs(x, i)) for i in range(1, n + 1)]
    return shares

# Fungsi untuk merekonstruksi rahasia
def recover_secret(shares, threshold):
    x_vals, y_vals = zip(*shares[:threshold])
    x = symbols('x')
    polynomial = lagrange_interpolation(x_vals, y_vals)
    secret = polynomial.subs(x, 0)
    return int(secret)

# Fungsi untuk melakukan interpolasi Lagrange
def lagrange_interpolation(x_vals, y_vals):
    x = symbols('x')
    polynomial = 0
    for j in range(len(x_vals)):
        numerator, denominator = Integer(1), Integer(1)
        for i in range(len(x_vals)):
            if i != j:
                numerator *= (x - x_vals[i])
                denominator *= (x_vals[j] - x_vals[i])
        term = y_vals[j] * numerator / denominator
        polynomial += term
    return polynomial.expand()

# Fungsi utama
def main():
    st.title("Simulasi Shamir's Secret Sharing")
    menu = st.sidebar.selectbox("Pilih Tahap:", ["Pembangkitan Kunci Rahasia", "Pembagian Kunci", "Distribusi Kunci", "Rekonstruksi Kunci"])

    if menu == "Pembangkitan Kunci Rahasia":
        st.header("Pembangkitan Kunci Rahasia")
        if st.button("Buat Kunci Rahasia"):
            secret_key = generate_secret_key()
            st.write(f"Kunci rahasia yang dihasilkan: {secret_key}")

    elif menu == "Pembagian Kunci":
        st.header("Pembagian Kunci Menggunakan Shamir's Secret Sharing")
        secret_key = st.text_input("Masukkan kunci rahasia:")
        n = st.number_input("Jumlah bagian:", value=5)
        k = st.number_input("Ambang batas untuk rekonstruksi:", value=3, min_value=1)
        if st.button("Bagi Kunci"):
            secret_key_int = int.from_bytes(secret_key.encode(), 'big')
            start_time = time.time()
            shares = split_secret(secret_key_int, n, k)
            end_time = time.time()
            st.write("Bagian-bagian rahasia yang dibagikan:")
            for share in shares:
                st.write(share)
            st.write(f"Waktu yang dibutuhkan untuk pembagian kunci: {end_time - start_time:.6f} detik")

    elif menu == "Distribusi Kunci":
        st.header("Distribusi Kunci kepada Pemegang Akun")
        pemegang_akun = st.text_area("Pemegang Akun (pisahkan dengan koma):")
        shares = st.text_area("Bagian-bagian Kunci (format: nomor bagian, nilai):", value=str(st.session_state.get('shares', '')))
        if st.button("Distribusi Kunci"):
            pemegang_akun_list = pemegang_akun.split(",")
            shares_list = [tuple(map(int, share.strip().strip("()").split(","))) for share in shares.split("\n") if share.strip()]
            distribusi = dict(zip(pemegang_akun_list, shares_list))
            st.write("Distribusi bagian kunci kepada pemegang akun:")
            for pemegang, bagian in distribusi.items():
                st.write(f"{pemegang.strip()}: {bagian}")

    elif menu == "Rekonstruksi Kunci":
        st.header("Rekonstruksi Kunci untuk Akses Akun")
        shares = st.text_area("Bagian-bagian Kunci (format: nomor bagian, nilai):").replace('(', '').replace(')', '')
        threshold = st.number_input("Jumlah bagian minimum yang diperlukan untuk merekonstruksi:", value=3, min_value=1)
        if st.button("Rekonstruksi Kunci"):
            shares = [tuple(map(int, share.strip().split(","))) for share in shares.splitlines() if share.strip()]
            start_time = time.time()
            reconstructed_key = recover_secret(shares, threshold)
            end_time = time.time()
            reconstructed_key = (reconstructed_key.to_bytes((reconstructed_key.bit_length() + 7) // 8, 'big')
                                 .decode('latin-1'))
            st.write(f"Rahasia yang direkonstruksi: {reconstructed_key}")
            st.write(f"Waktu yang dibutuhkan untuk rekonstruksi kunci: {end_time - start_time:.6f} detik")


if __name__ == "__main__":
    main()
