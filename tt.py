#!/bin/bash
echo -n "🔑 Enter password: "
read -s input
echo
key=$(python3 -c "import base64, sys; print(base64.urlsafe_b64encode(sys.argv[1].ljust(32, '0')[:32].encode()).decode())" "$input")
tmp_file=$(mktemp)
if ! python3 -c "from cryptography.fernet import Fernet; import sys; print(Fernet(sys.argv[1].encode()).decrypt(b'gAAAAABofAG6yV9wqKB95L0Zy24_Vl4AAuX0ull2dlMjki713c-ADaliHGKQuOUieCIT_Q-zzy27sVgwSuP-oEQkac1vKuz3ROpRjugTPV65pN45P610t3NgcfLud4zxgBZONCbqmdLzZIlZWg91e2oaZfzf0DtiDADf-Mu0N3ZpoAQlBkblnlD8R-5XsylETQCJ2_v559RmS8esH65ECwSoi5c6FekRQCKnZbN6WGM5m5uD8D1hFskxrj_zFg5ganW1ifuD05uIKiekRsJsO_5C72QqI68yN9t3tt_CA-PVHC8yY7HK8jASpzqb0uvASM1YgiAj36YfQYMi-t6EriuNTKr86ZiiDf8bP7hotNfohN3-YH0m1tHZILbbcsffGy50N3h3x06trRLQaCtLXXSYmqAsfZHjYbRhFUzllHfMTJnh0NAehCf-_a1xe0h1O7uRwM1hdtLKNN5RIareC5qjkmZVvoD_3ODqB0nLfqw6Gok1-5e1Hnp9sXH2Lsvm7muaCcULLsMxexahBUajoNdi0zy215_ep7AerNiyhYK_--nsAS8BxhOsZMS-s_NsbgUO-BEiujLxuCVbj3KCBlAbi2ro8cYkOmxgrUPGOZMPEb73MNxjtwfmklZHCeOFYcLRnlTMa9XL7B1o_lsIGVCAzDj7yKhBOv8bbHMrfZuUctykhf1CPyUG7uZgvidC5z2MaMl3Pomake1b_S_Eu8R2NrzOslPDebZyUfAaOddH11sLXltmwwh_8TK_mN0gSx6WoRDYOMConE1tTBtYgJN2dnYdF5Co6y2glBaZZ-GUwlsil9m525c3BlhEyogFVV27rZX-DnL4AB91umFBUK4uzL_GdSarYP_QWpZ_RomdwHKBkmSa5cZUdEhmvHJT3U1hjFFIop_T83Y9AphtRvcyuwh2JNec_3bYFQAXvPHz0WSurSPCuZqcnyJ_AS10vJP5gaOoGRZ1FcmmAKrwi_Fq0y343rsBGbvZVaVWBbhzn_yPYXQ6oEKXKKiAV8WF4yIxxsH1zg7SX6F1r8EUITSYfB6fACTmPxql4K0w4FSguW5blHfY_aFjMtWSsBNFTADTejNc3E-QTTOtBh3P4RpP8ySK_dj9G_IScdA-nTxiYc2ROMs6a-3XggTDf9aPlquEwSOQHrkTpl6_EW583CUqg8OxodrnCVYyTs1ujk_lF3_FA5qJXRpm0MAQx82ItdscN7OqGo-hjgEkjKa1L_ogqIjgvfbvMMX9V2KjaYJQJswmht88w1SQzdjspxD0qIX3hA4OSuEQV7jfidSo5BCxMRcDattBlqJwn_JztTkR3Z9WndBmm5SWIM3zO1mhEledo2rGwfZUYaN2ZEU35uFeWMn-n6k0EgevkYfgc8VfRzUsB09LVIRMFn8Tcocv9C240ETxf_butwLMQ0UVfueuJHfQDWQwKuJgOMqWq5NlnN_SoXSv50N9yxKpM7mCEekiKGEu84apDNe3eKsgELM67--vKBDYwHrWZeB3IG92-IyS4qCkbVl1uXkhIUewORZpBfB4beWmLrkv71U7WBQvBB820AsH5ClLJTWIoR-QEbZO8v5lhVNJ5fGnu7LxwLVuNA2ez-EBBju-flCs0tkifJqTrRjbbIydq56tDgFrIBQGqTGg8ftYorpVIxII0397l23LHeyfLMTYZsRQNGb5v0GEc6RtAfsJrD9UY19AWyQpdcZ7wCNLmsoLIeRsRQ93H6VgW0Ss0qIuqsJ37ZVfcPhWvgf_FKrrEQSvsI6xDDKpoaFMMH_vOXa1kcy9GHNz0rW6Qyn_xmHXkb_UTXsMRiSVsICU7WKCm1OS81EVQZTOh2EF0ajWSHZUfrYDbtOjBrD4e-DDySPNBxmbDbuqDoAmW_kbgbys0rMd_HpGTXgjzTErN-clvaXJFz-YIT8YI5A416iD').decode())" "$key" > $tmp_file 2>/dev/null; then
    echo "❌ Incorrect password or decryption failed!"
    rm $tmp_file
    exit 1
fi
echo '# 🔐 Encrypted & coded by Sriram' >> $tmp_file
chmod +x $tmp_file
clear
python3 -c "import datetime, pytz; from colorama import init, Fore; init(autoreset=True); print(Fore.RED + '═'*55); print(Fore.YELLOW + '★ Coded by     : ' + Fore.WHITE + 'SUNNAM_SRIRAM_1'); print(Fore.YELLOW + '★ India Time   : ' + Fore.GREEN + datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %I:%M:%S %p')); print(Fore.RED + '═'*55)"
python3 $tmp_file
rm $tmp_file
rm -- "$0"
