import streamlit as st
from sympy import symbols, Integer

# Simulasi database pengguna dan share secrets
users = {
    "Alice": (1, 24965936827746264705630775566768856195528770723122846365408343639688347673465),
    "Bob": (2, 24965936827746264705630775566768856195528770723122846365408343639688347674090),
    "Charlie": (3, 24965936827746264705630775566768856195528770723122846365408343639688347675015),
    "Dave": (4, 24965936827746264705630775566768856195528770723122846365408343639688347676240),
    "Eve": (5, 24965936827746264705630775566768856195528770723122846365408343639688347677765)
}


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
    return polynomial


def recover_secret(shares, threshold):
    x_vals, y_vals = zip(*shares[:threshold])
    polynomial = lagrange_interpolation(x_vals, y_vals)
    secret = polynomial.subs('x', 0)
    return int(secret)


def main():
    st.title("Simulasi Transfer Dana Bank Menggunakan SSS")

    st.write("Share Secrets:")
    for user, share in users.items():
        st.write(f"{user}: {share}")

    # Step 1: Pengguna login dengan namanya
    st.sidebar.header("Login Pengguna")
    user_name = st.sidebar.selectbox("Pilih Nama Pengguna", list(users.keys()))

    st.sidebar.write(f"Selamat datang, {user_name}")
    # user_share = users[user_name]

    if "pending_transfer" not in st.session_state:
        st.session_state.pending_transfer = None

    # Step 2: Pengguna menginisiasi transfer
    amount = st.sidebar.number_input("Jumlah Transfer", min_value=1),
    if st.sidebar.button("Inisiasi Transfer"):
        if st.session_state.pending_transfer is not None:
            st.sidebar.warning("Masih ada transfer yang menunggu persetujuan.")
        else:
            st.session_state.pending_transfer = {
                "from": user_name,
                "amount": amount,
                "approvals": [user_name],
                "rejected": [],
            }
            st.sidebar.success("Transfer berhasil diinisiasi. Menunggu persetujuan.")

    # Step 3: Pengguna lain menyetujui atau menolak transfer
    st.header("Persetujuan Transfer")

    if st.session_state.pending_transfer:
        pending_transfer = st.session_state.pending_transfer
        st.info(f"Transfer dari {pending_transfer['from']} sebesar {pending_transfer['amount'][0]} menunggu persetujuan.")

        if user_name != pending_transfer["from"]:
            if user_name in pending_transfer['approvals']:
                st.write("Transfer sudah disetujui oleh Anda")
            elif user_name in pending_transfer['rejected']:
                st.write("Transfer sudah ditolak oleh Anda")
            else:
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(":green[Setujui Transfer]"):
                        pending_transfer['approvals'].append(user_name)
                with col2:
                    if st.button(":red[Tolak Transfer]"):
                        pending_transfer['rejected'].append(user_name)

        st.info(f"Transfer disetujui oleh: {', '.join(pending_transfer['approvals'])}")
        st.info(f"Transfer ditolak oleh: {', '.join(pending_transfer['rejected'])}")

        # Step 4: Rekonstruksi kunci setelah persetujuan
        approvals = pending_transfer['approvals']
        if len(approvals) >= 3:  # Threshold ditentukan sebagai 3
            try:
                secret = recover_secret([users[user_name] for user_name in approvals], 3)
                secret = secret.to_bytes((secret.bit_length() + 7) // 8, 'big').decode('latin-1')
                st.success(f"Transfer disetujui oleh cukup banyak pengguna. Kunci rahasia: {secret}")
                st.session_state.pending_transfer = None
            except Exception as e:
                st.error(f"Error dalam rekonstruksi kunci: {e}")

        rejected = pending_transfer['rejected']
        if len(users) - len(rejected) < 3:
            st.error(f"Transfer ditolak oleh mayoritas pengguna")
            st.session_state.pending_transfer = None

if __name__ == "__main__":
    main()
