#!/bin/bash
# =============================================
# ✅ Encrypted Script
# ★ Coded by     : SUNNAM_SRIRAM_1
# ★ India Time   : 2025-07-20 02:11:16 AM
# =============================================
echo -n "🔑 Enter password: "
read -s input
echo
key=$(python3 -c "import base64, sys; print(base64.urlsafe_b64encode(sys.argv[1].ljust(32, '0')[:32].encode()).decode())" "$input")
tmp_file=$(mktemp)
if ! python3 -c "from cryptography.fernet import Fernet; import sys; print(Fernet(sys.argv[1].encode()).decrypt(b'gAAAAABofALsO175aSHIk2q6PYZHd3OzfpMPTvGH1Fcc8xQeTm8EnspOaxRXJt2Y1OTVPw6MwAGi9A0sT-0Qg0Jb7Jyk9a3o69tNrGfKpEtO6771H6GpdMJMS7GbmH-8jq5sb4-aJ3DVm7T7W_96yOdZqE1EuCKk21K36K9u6I-EfJWsKq2QnvzJnSGO4pCSJKxnFs4iUo-Ia9_ppgxMKiaP4tdy-qdhwztQC3VXEKQHIBh0xVIfKQslX7K3oxOyVJxxpLcIube4rFj3Efr_u8eIfsb6vVmEhIWqo6qBxuhSB7-Q1qhvzx0cysE-ixR-Mcgvo5H4E2eSRkNVheFfidF2UZ5qP7dN_8T1nxZjA5YWsX5t175_nXnnwEP6JagoxTuhLebzCYskI82CXhMI6dAe8lNpPNRjyLle-8-0v1AOMiaLk49FnTKwrpuNHrBhkaAMJ5tiextatZRWL56H0Q2cUt_S0ozd7eCVjLtNIWyzS9nGrCzPTIibXzh-gkPJ5QaAqPNbfO4Pge0ngYiosOIS6BOQPOG0QFmhBao-78JcBr6ygTgKLmvOc0fNoszTvSHtoe0QwcRSVd9ecmCgB_dkFBMIuI1RSDm_AHbLnLpgRXvuWBIGjTqWfgFA5MyemcUj7wQjuxekLEjCf9peeW3VtL5lYCYUh7hdQD6KM1aZ6KkN4yAXilnVgmdHFkXAlhOsApSx-Dfs-OL1HtNhWue6wsqlmkl0751FG4O5QoxvhHq23PNl0-holOJk2zYcc7u5550xkIRXxTH3kBJRm5AChiJLYbvlSmC7qm6DS5rkD5symSTBPAcQ32ZpWWWiI7q74LjO5SgplJZVMXHKUas2TVYp_jOiFblFYkMCU0QQEyJ1MFF9nDefe7Mq41ljYaQt9uZUE266ximExB4eZ3wXE1-4T0OSO1fM7YP4QUZKFMRqq3CeeHX0z9CfppDWkWgADZsgQk2DID034w6930nsZs6ph9q5xFEkFV2YR4Z4haqmqnZHd7EkHOuU-KgIZKcSzeRDLaFmK5gKpfyuaUpl0iQGwf6BnS8VzAttUlq_acbmATxk9Qx0MiB8FDCyo9MkaXwmggUjFDcTDX_SgtRuTLgF6iAImGqYAQhNz8-mbX-l1c7B_9BbKb4cpqbNtukbZ0nGTehE-W-b134Z1_P7Ys0T_KY5BGC0K-3Wlch0s6RYojeeuXV6SuRRWhZ9jgvmNX6leXCRhMgsvP2HcfNBxbXMTDjGFxjPctcrMNAcNUDM3sECH8gJm5lIpvARkdWL1PBc854ZtlL7kt3pbJ34I0cYULcipLuEauxKAwcpfu808TXfz0T6zm7P9pPccC4VMyb71apfUjJIaoQx5PkGIuYMZd88xnbyq_kuQcwmn1IOS9sKsqxMgiBhyRFqQKbRlmiovLPkmZTq-ccgOsA0iB9mrqNGa_B2TQoIATeg0NuWkXdW4kFVppsvVrxJm2ev7goenAaf3nGM8PrvA9PpLK4aLVeBHnXPpB8RD8ph5FaRzXe7WnlfBEP1xz53UVM-W-VzBYvcJSfrcBh4xteTmQQD0gvMa6u4et5sAyNeu829YwZRA9CGvreTRcliXScvZXmRTvl47wPZVxnkD_N3BbQoeSnfFz2NrDJYhq3qK4gJKT-TTeqIPrGJXw3CZ7nagdxLvmaHHbA3Aoak-UaeKUDMu4ajRB_IFAQT5hnapE6ldfp4At12nEFkpeqsnL1Q_vwlYYuoccvIe3oB5qjfWf6e_e0ZO3f8Dd0j8fCfBLl0chUO44BXQsC4gbOXYq13hs4xtVXz95BiX9TmNLUpI7bwawLTmOmIkpnNVKaHiKJzzYuPJvmfEeY-PYsrEun-JjEKQo66R6ulYK-vK-7t9SfOHNOd0e0j25H3S6DZNGwNyjL3etzo-JTDBRpQyOnSGkOcpc1q').decode())" "$key" > $tmp_file 2>/dev/null; then
    echo "❌ Incorrect password or decryption failed!"
    rm $tmp_file
    exit 1
fi
echo '# 🔐 Encrypted & coded by Sriram' >> $tmp_file
chmod +x $tmp_file
python3 $tmp_file
rm $tmp_file
rm -- "$0"
