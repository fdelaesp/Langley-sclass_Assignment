import streamlit as st

st.set_page_config(page_title="CNT4603 Visitor Setup Guide", page_icon="🐧", layout="wide")

st.title("🐧 CNT4603 Visitor Setup — Arch Linux Lab Guide")
st.caption("School lab computer (host) + QEMU guest VM. All paste happens as user0 in the host GUI terminal.")

st.sidebar.header("📋 All Steps")
st.sidebar.markdown("""
**HOST MACHINE SETUP**
- [Step 0: Install Dependencies](#step-0-install-dependencies)
- [Step 1: Create Working Directory](#step-1-create-working-directory)
- [Step 2: Create newusers.txt](#step-2-create-newusers-txt)
- [Step 3: Create add_visitors.sh](#step-3-create-add-visitors-sh)
- [Step 4: Create setup_testuser.sh](#step-4-create-setup-testuser-sh)
- [Step 5: Create verify_users.sh](#step-5-create-verify-users-sh)
- [Step 6: Create remove_visitors.sh](#step-6-create-remove-visitors-sh)
- [Step 7: Make Scripts Executable](#step-7-make-all-scripts-executable)
- [Step 8: Generate SSH Host Keys](#step-8-generate-ssh-host-keys-arch-requirement)
- [Step 9: Enable sshd](#step-9-enable-and-start-sshd)
- [Step 10: Configure sshd_config](#step-10-configure-sshd-config)
- [Step 11: Restart sshd](#step-11-restart-sshd)
- [Step 12: Run Main Script](#step-12-run-the-main-script)
- [Step 13: Generate Test Keypair](#step-13-generate-test-keypair)
- [Step 14: Install Test Key](#step-14-install-testuser-key)
- [Step 15: Verify All Users](#step-15-verify-all-users)
- [Step 16: Find Host IP](#step-16-find-host-ip-for-ssh-test)

**SSH TEST FROM QEMU GUEST**
- [Step 17: Test SSH from Guest](#step-17-test-ssh-from-qemu-guest-into-host)

**GUEST VM SETUP**
- [Step 18: Set Up Guest VM](#step-18-set-up-guest-vm)
- [Step 19: Cleanup (if needed)](#step-19-cleanup-if-you-need-to-redo)
""")

st.divider()
st.info("""💡 **YOUR LAB SETUP:**
- **Host** = school lab computer running Arch Linux (has root via sudo, has Firefox for paste)
- **Guest** = QEMU virtual machine running Arch Linux
- You paste commands from Firefox into the **host** terminal as **user0**, using `sudo` for root commands
- SSH test = from the **QEMU guest** into the **host**""")

st.divider()

# ════════════════════════════════════════════════════════════════
# HOST MACHINE SETUP
# ════════════════════════════════════════════════════════════════

st.subheader("═══ HOST MACHINE SETUP ═══")

st.divider()

# ════════════════════════════════════════════
# STEP 0
# ════════════════════════════════════════════
st.header("Step 0: Install Dependencies")
st.write("Open a terminal on the **host** as **user0** and run:")
st.code("sudo pacman -Syu", language="bash")
st.code("sudo pacman -S --needed wget openssh zsh", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 1
# ════════════════════════════════════════════
st.header("Step 1: Create Working Directory")
st.write("As **user0** on the host:")
st.code("mkdir -p ~/visitors", language="bash")
st.code("cd ~/visitors", language="bash")
st.warning("⚠️ Run **ALL** remaining host steps from inside `~/visitors/`")

st.divider()

# ════════════════════════════════════════════
# STEP 2
# ════════════════════════════════════════════
st.header("Step 2: Create newusers.txt")
st.write("As **user0** on the host, paste this entire block:")
st.code("""cat > ~/visitors/newusers.txt << 'EOF'
adams:5000:Adams, John Couch:/bin/bash
atiyah:5001:Atiyah, Michael:/bin/zsh
babbage:5002:Babbage, Charles:/bin/zsh
baker:5003:Baker, Alan:/bin/zsh
barrow:5004:Barrow, Isaac:/bin/bash
birch:5005:Birch, Bryan John:/bin/zsh
borcherds:5006:Borcherds, Richard Ewen:/bin/bash
cartwright:5007:Cartwright, Dame Mary:/bin/zsh
cayley:5008:Cayley, Arthur:/bin/zsh
clifford:5009:Clifford, William Kingdon:/bin/zsh
coates:5010:Coates, John:/bin/bash
conway:5011:Conway, John Horton:/bin/zsh
cotes:5012:Cotes, Roger:/bin/bash
daniell:5013:Daniell, Percy John:/bin/zsh
dawid:5014:Dawid, Philip:/bin/zsh
davenport:5015:Davenport, Harold:/bin/zsh
davidson:5016:Davidson, Rollo:/bin/bash
donaldson:5017:Donaldson, Simon:/bin/zsh
dirac:5018:Dirac, Paul:/bin/zsh
eddington:5019:Eddington, Arthur Stanley:/bin/bash
forsyth:5020:Forsyth, Andrew:/bin/bash
glaisher:5021:Glaisher, James:/bin/bash
goddard:5022:Goddard, Peter:/bin/zsh
gowers:5023:Gowers, William Timothy:/bin/bash
grimmett:5024:Grimmett, Geoffrey:/bin/zsh
grojnowski:5025:Grojnowski, Ian:/bin/bash
hawking:5026:Hawking, Stephen:/bin/bash
hitchin:5027:Hitchin, Nigel:/bin/zsh
jeans:5028:Jeans, James:/bin/bash
jeffreys:5029:Jeffreys, Harold:/bin/bash
jones:5030:Jones, Thomas:/bin/bash
kelly:5031:Kelly, Frank:/bin/zsh
kendall:5032:Kendall, David George:/bin/zsh
king:5033:King, Joshua:/bin/bash
kirwan:5034:Kirwan, Frances:/bin/zsh
larmor:5035:Larmor, Joseph:/bin/bash
leader:5036:Leader, Imre:/bin/zsh
littlewood:5037:Littlewood, John Edensor:/bin/bash
maxwell:5038:Maxwell, James Clerk:/bin/bash
macalister:5039:MacAlister, Donald:/bin/bash
newman:5040:Newman, Max:/bin/zsh
milner:5041:Milner, Isaac:/bin/bash
newton:5042:Newton, Isaac:/bin/bash
norris:5043:Norris, James:/bin/bash
norton:5044:Norton, Simon:/bin/bash
orr:5045:Orr, William McFadden:/bin/zsh
penrose:5046:Penrose, Roger:/bin/bash
ramanujan:5047:Ramanujan, Srinivasa:/bin/zsh
ramsey:5048:Ramsey, Frank:/bin/bash
rogers:5049:Rogers, Chris:/bin/bash
russell:5050:Russell, Bertrand:/bin/zsh
segal:5051:Segal, Graeme:/bin/bash
spiegelhalter:5052:Spiegelhalter, David:/bin/bash
stokes:5053:Stokes, Sir George Gabriel:/bin/bash
sylvester:5054:Sylvester, James Joseph:/bin/zsh
taylor:5055:Taylor, Martin:/bin/zsh
thompson:5056:Thompson, John:/bin/bash
turing:5057:Turing, Alan:/bin/zsh
venn:5058:Venn, John:/bin/zsh
wallis:5059:Wallis, John:/bin/bash
weber:5060:Weber, Richard:/bin/zsh
whitehead:5061:Whitehead, Alfred North:/bin/zsh
whittle:5062:Whittle, Peter:/bin/zsh
wiles:5063:Wiles, Andrew:/bin/bash
williams:5064:Williams, David:/bin/bash
wylie:5065:Wylie, Shaun:/bin/bash
zeeman:5066:Zeeman, Erik Christopher:/bin/bash
johri:5067:Johri, Vinod:/bin/zsh
testuser:5099:Test User, SSH Verification:/bin/bash
EOF""", language="bash")

st.write("Verify it was created:")
st.code("wc -l ~/visitors/newusers.txt", language="bash")
st.info("You should see **69** (68 real users + 1 testuser).")

st.divider()

# ════════════════════════════════════════════
# STEP 3
# ════════════════════════════════════════════
st.header("Step 3: Create add_visitors.sh")
st.write("As **user0** on the host, paste this entire block:")
st.code(r"""cat > ~/visitors/add_visitors.sh << 'SCRIPTEOF'
#!/bin/bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <userfile> <pubkey_base_url>"
    exit 1
fi

USERFILE="$1"
PUBKEY_URL="$2"
[[ "${PUBKEY_URL}" != */ ]] && PUBKEY_URL="${PUBKEY_URL}/"

if [[ ! -f "$USERFILE" ]]; then
    echo "ERROR: '$USERFILE' not found."
    exit 1
fi

mkdir -p /home/visitors
mkdir -p /scratch

if [[ ! -f /etc/ssh/ssh_host_rsa_key ]]; then
    echo ">>> Generating SSH host keys (Arch requirement)..."
    ssh-keygen -A
fi

echo ">>> Ensuring sshd is enabled..."
systemctl enable sshd 2>/dev/null || true
systemctl start sshd 2>/dev/null || true

while IFS=: read -r name uid gecos shell; do
    [[ -z "$name" || "$name" == \#* ]] && continue
    name="$(echo "$name" | xargs)"
    uid="$(echo "$uid" | xargs)"
    gecos="$(echo "$gecos" | xargs)"
    shell="$(echo "$shell" | xargs)"

    HOMEDIR="/home/visitors/${name}"
    SCRATCHDIR="/scratch/${name}"

    echo "============================================"
    echo "Processing: $name (uid=$uid)"
    echo "============================================"

    if id "$name" &>/dev/null; then
        echo "  WARNING: User '$name' exists. Skipping."
        continue
    fi
    if getent group "$name" &>/dev/null; then
        echo "  WARNING: Group '$name' exists. Skipping."
        continue
    fi

    groupadd -g "$uid" "$name"

    useradd \
        -u "$uid" \
        -g "$name" \
        -d "$HOMEDIR" \
        -m \
        -k /etc/skel \
        -s "$shell" \
        -c "$gecos" \
        "$name"

    passwd -l "$name" 2>/dev/null || true

    chown "$name":"$name" "$HOMEDIR"
    chmod 700 "$HOMEDIR"

    mkdir -p "${HOMEDIR}/.ssh"
    chown "$name":"$name" "${HOMEDIR}/.ssh"
    chmod 700 "${HOMEDIR}/.ssh"

    PUBKEY_FILE="${PUBKEY_URL}${name}.pub"
    echo "  Fetching: $PUBKEY_FILE"
    if wget -q -O "${HOMEDIR}/.ssh/authorized_keys" "$PUBKEY_FILE" 2>/dev/null; then
        echo "  SUCCESS: Pubkey installed."
    else
        echo "  NOTICE: No pubkey for $name."
        touch "${HOMEDIR}/.ssh/authorized_keys"
    fi

    chown "$name":"$name" "${HOMEDIR}/.ssh/authorized_keys"
    chmod 600 "${HOMEDIR}/.ssh/authorized_keys"

    mkdir -p "$SCRATCHDIR"
    chown "$name":"$name" "$SCRATCHDIR"
    chmod 700 "$SCRATCHDIR"

    echo "  Done: $name"
    echo ""
done < "$USERFILE"

echo "============================================"
echo "ALL USERS PROCESSED."
echo "============================================"
SCRIPTEOF""", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 4
# ════════════════════════════════════════════
st.header("Step 4: Create setup_testuser.sh")
st.write("As **user0** on the host, paste:")
st.code(r"""cat > ~/visitors/setup_testuser.sh << 'SCRIPTEOF'
#!/bin/bash
set -euo pipefail
KEYDIR="$HOME/testkeys"
mkdir -p "$KEYDIR"

echo ">>> Generating SSH keypair for testuser..."
ssh-keygen -t ed25519 -f "${KEYDIR}/testuser_key" -N "" -C "testuser@test"

echo ""
echo "Keys generated:"
echo "  Private: ${KEYDIR}/testuser_key"
echo "  Public:  ${KEYDIR}/testuser_key.pub"
echo ""
cat "${KEYDIR}/testuser_key.pub"
SCRIPTEOF""", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 5
# ════════════════════════════════════════════
st.header("Step 5: Create verify_users.sh")
st.write("As **user0** on the host, paste:")
st.code(r"""cat > ~/visitors/verify_users.sh << 'SCRIPTEOF'
#!/bin/bash
set -uo pipefail
if [[ $# -ne 1 ]]; then echo "Usage: $0 <userfile>"; exit 1; fi
USERFILE="$1"; ERRORS=0
echo "Verifying from: $USERFILE"
echo "============================================"
while IFS=: read -r name uid gecos shell; do
    [[ -z "$name" || "$name" == \#* ]] && continue
    name="$(echo "$name" | xargs)"; uid="$(echo "$uid" | xargs)"
    HOMEDIR="/home/visitors/${name}"; SCRATCHDIR="/scratch/${name}"
    echo ""; echo "--- $name (uid=$uid) ---"
    if ! id "$name" &>/dev/null; then
        echo "  FAIL: User missing"; ((ERRORS++)); continue; fi
    AUID=$(id -u "$name")
    [[ "$AUID" == "$uid" ]] && echo "  OK: UID=$uid" || { echo "  FAIL: UID=$AUID expected=$uid"; ((ERRORS++)); }
    AGID=$(id -g "$name")
    [[ "$AGID" == "$uid" ]] && echo "  OK: GID=$uid" || { echo "  FAIL: GID=$AGID expected=$uid"; ((ERRORS++)); }
    if [[ -d "$HOMEDIR" ]]; then
        P=$(stat -c '%a' "$HOMEDIR"); O=$(stat -c '%U:%G' "$HOMEDIR")
        [[ "$P" == "700" ]] && echo "  OK: home=700" || { echo "  FAIL: home=$P"; ((ERRORS++)); }
        [[ "$O" == "${name}:${name}" ]] && echo "  OK: home owner=$O" || { echo "  FAIL: home owner=$O"; ((ERRORS++)); }
    else echo "  FAIL: home missing"; ((ERRORS++)); fi
    SD="${HOMEDIR}/.ssh"
    if [[ -d "$SD" ]]; then
        P=$(stat -c '%a' "$SD"); O=$(stat -c '%U:%G' "$SD")
        [[ "$P" == "700" ]] && echo "  OK: .ssh=700" || { echo "  FAIL: .ssh=$P"; ((ERRORS++)); }
        [[ "$O" == "${name}:${name}" ]] && echo "  OK: .ssh owner=$O" || { echo "  FAIL: .ssh owner=$O"; ((ERRORS++)); }
    else echo "  FAIL: .ssh missing"; ((ERRORS++)); fi
    AK="${SD}/authorized_keys"
    if [[ -f "$AK" ]]; then
        P=$(stat -c '%a' "$AK"); O=$(stat -c '%U:%G' "$AK")
        [[ "$P" == "600" ]] && echo "  OK: ak=600" || { echo "  FAIL: ak=$P"; ((ERRORS++)); }
        [[ "$O" == "${name}:${name}" ]] && echo "  OK: ak owner=$O" || { echo "  FAIL: ak owner=$O"; ((ERRORS++)); }
        [[ -s "$AK" ]] && echo "  OK: has pubkey" || echo "  WARN: ak empty"
    else echo "  FAIL: ak missing"; ((ERRORS++)); fi
    if [[ -d "$SCRATCHDIR" ]]; then
        O=$(stat -c '%U:%G' "$SCRATCHDIR")
        [[ "$O" == "${name}:${name}" ]] && echo "  OK: scratch=$O" || { echo "  FAIL: scratch=$O"; ((ERRORS++)); }
    else echo "  FAIL: scratch missing"; ((ERRORS++)); fi
done < "$USERFILE"
echo ""; echo "============================================"
[[ $ERRORS -eq 0 ]] && echo "ALL CHECKS PASSED" || echo "ERRORS: $ERRORS"
SCRIPTEOF""", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 6
# ════════════════════════════════════════════
st.header("Step 6: Create remove_visitors.sh")
st.write("As **user0** on the host, paste:")
st.code(r"""cat > ~/visitors/remove_visitors.sh << 'SCRIPTEOF'
#!/bin/bash
set -uo pipefail
if [[ $# -ne 1 ]]; then echo "Usage: $0 <userfile>"; exit 1; fi
USERFILE="$1"
while IFS=: read -r name uid gecos shell; do
    [[ -z "$name" || "$name" == \#* ]] && continue
    name="$(echo "$name" | xargs)"
    echo "Removing: $name"
    userdel "$name" 2>/dev/null || true
    groupdel "$name" 2>/dev/null || true
    rm -rf "/home/visitors/${name}" 2>/dev/null || true
    rm -rf "/scratch/${name}" 2>/dev/null || true
done < "$USERFILE"
echo "Done. All visitors removed."
SCRIPTEOF""", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 7
# ════════════════════════════════════════════
st.header("Step 7: Make All Scripts Executable")
st.write("As **user0** on the host:")
st.code("chmod +x ~/visitors/add_visitors.sh", language="bash")
st.code("chmod +x ~/visitors/setup_testuser.sh", language="bash")
st.code("chmod +x ~/visitors/verify_users.sh", language="bash")
st.code("chmod +x ~/visitors/remove_visitors.sh", language="bash")

st.write("Verify:")
st.code("ls -la ~/visitors/", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 8
# ════════════════════════════════════════════
st.header("Step 8: Generate SSH Host Keys (Arch Requirement)")
st.error("🔴 Required on Arch Linux before sshd works.")
st.write("As **user0** on the host:")
st.code("sudo ssh-keygen -A", language="bash")

st.write("Verify:")
st.code("ls -la /etc/ssh/ssh_host_*", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 9
# ════════════════════════════════════════════
st.header("Step 9: Enable and Start sshd")
st.write("As **user0** on the host:")
st.code("sudo systemctl enable sshd", language="bash")
st.code("sudo systemctl start sshd", language="bash")
st.code("sudo systemctl status sshd", language="bash")
st.success("You should see **active (running)**.")

st.divider()

# ════════════════════════════════════════════
# STEP 10
# ════════════════════════════════════════════
st.header("Step 10: Configure sshd_config")
st.write("As **user0** on the host, check current setting:")
st.code("grep -i 'PubkeyAuthentication' /etc/ssh/sshd_config", language="bash")

st.write("Fix it (works whether it's commented out or set to no):")
st.code("sudo sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config", language="bash")

st.write("If grep showed **nothing at all**, add it:")
st.code('echo "PubkeyAuthentication yes" | sudo tee -a /etc/ssh/sshd_config', language="bash")

st.write("Verify:")
st.code("grep -i 'PubkeyAuthentication' /etc/ssh/sshd_config", language="bash")
st.success("Should show: `PubkeyAuthentication yes`")

st.divider()

# ════════════════════════════════════════════
# STEP 11
# ════════════════════════════════════════════
st.header("Step 11: Restart sshd")
st.write("As **user0** on the host:")
st.code("sudo systemctl restart sshd", language="bash")
st.code("sudo systemctl status sshd", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 12
# ════════════════════════════════════════════
st.header("Step 12: Run the Main Script")
st.error("🔴 This creates all 69 user accounts on the **host**.")
st.write("As **user0** on the host:")
st.code("cd ~/visitors", language="bash")
st.code("sudo bash ~/visitors/add_visitors.sh ~/visitors/newusers.txt https://www.cs.fsu.edu/~langley/NEWKEYS/", language="bash")

st.write("Watch the output:")
st.write("- **SUCCESS: Pubkey installed** = user had a pubkey on the server")
st.write("- **NOTICE: No pubkey for X** = user didn't provide one (expected per assignment)")

st.write("Spot-check a few users:")
st.code("id adams", language="bash")
st.code("id turing", language="bash")
st.code("id testuser", language="bash")
st.code("ls -la /home/visitors/adams/", language="bash")
st.code("ls -la /home/visitors/adams/.ssh/", language="bash")
st.code("ls -la /scratch/adams/", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 13
# ════════════════════════════════════════════
st.header("Step 13: Generate Test Keypair")
st.write("As **user0** on the host (no sudo — keys go in your home dir):")
st.code("bash ~/visitors/setup_testuser.sh", language="bash")

st.write("Verify keys exist:")
st.code("ls -la ~/testkeys/", language="bash")
st.info("`testuser_key` = private key, `testuser_key.pub` = public key")

st.divider()

# ════════════════════════════════════════════
# STEP 14
# ════════════════════════════════════════════
st.header("Step 14: Install testuser Key")
st.write("As **user0** on the host, install the public key into testuser's account:")
st.code("sudo cp ~/testkeys/testuser_key.pub /home/visitors/testuser/.ssh/authorized_keys", language="bash")
st.code("sudo chown testuser:testuser /home/visitors/testuser/.ssh/authorized_keys", language="bash")
st.code("sudo chmod 600 /home/visitors/testuser/.ssh/authorized_keys", language="bash")

st.write("Verify:")
st.code("sudo cat /home/visitors/testuser/.ssh/authorized_keys", language="bash")
st.code("sudo stat -c '%a %U:%G' /home/visitors/testuser/.ssh/authorized_keys", language="bash")
st.success("Should show: `600 testuser:testuser`")

st.divider()

# ════════════════════════════════════════════
# STEP 15
# ════════════════════════════════════════════
st.header("Step 15: Verify All Users")
st.write("As **user0** on the host:")
st.code("sudo bash ~/visitors/verify_users.sh ~/visitors/newusers.txt", language="bash")

st.write("What the output means:")
st.write("- **OK** = check passed")
st.write("- **WARN: ak empty** = no pubkey on the server (expected for some users)")
st.write("- **FAIL** = fix it")
st.write("- **ALL CHECKS PASSED** = you're good!")

st.divider()

# ════════════════════════════════════════════
# STEP 16
# ════════════════════════════════════════════
st.header("Step 16: Find Host IP for SSH Test")
st.write("On the **host**, find the IP address the QEMU guest can reach:")
st.code("ip addr show", language="bash")
st.info("Look for an IP on your network interface (e.g. `192.168.x.x` or `10.0.x.x`). Write it down — you'll need it in the next step.")

st.write("Also test SSH works locally on the host first:")
st.code("ssh -i ~/testkeys/testuser_key testuser@localhost", language="bash")
st.write("If it asks about the fingerprint, type **yes**. You should get a shell without a password.")
st.write("Once verified, type:")
st.code("exit", language="bash")

st.divider()

# ════════════════════════════════════════════════════════════════
# SSH TEST FROM QEMU GUEST
# ════════════════════════════════════════════════════════════════

st.subheader("═══ SSH TEST FROM QEMU GUEST ═══")

st.divider()

# ════════════════════════════════════════════
# STEP 17
# ════════════════════════════════════════════
st.header("Step 17: Test SSH from QEMU Guest into Host")
st.write("First, you need to get the testuser private key onto the QEMU guest. From the **host** as **user0**:")
st.write("")
st.write("**Option A: SCP the key from host to guest** (if guest has sshd running):")
st.code("scp ~/testkeys/testuser_key user0@GUEST_IP:/home/user0/testuser_key", language="bash")

st.write("**Option B: If guest doesn't have sshd yet**, use a shared folder or manually type the key.")
st.write("")
st.write("Once the private key is on the **guest**, open a terminal on the guest and run:")
st.code("chmod 600 ~/testuser_key", language="bash")
st.code("ssh -i ~/testuser_key testuser@HOST_IP", language="bash")
st.warning("⚠️ Replace `HOST_IP` with the actual IP you found in Step 16.")

st.write("If it asks about the fingerprint, type **yes**.")
st.write("")
st.write("Once logged in, verify everything:")
st.code("whoami", language="bash")
st.code("id", language="bash")
st.code("pwd", language="bash")
st.code("ls -la ~", language="bash")
st.code("ls -la ~/.ssh", language="bash")
st.code("ls -la ~/.ssh/authorized_keys", language="bash")
st.code("ls -la /scratch/testuser", language="bash")

st.success("✅ If you got a shell as `testuser` **without a password prompt**, SSH pubkey auth is working!")

st.code("exit", language="bash")

st.write("---")
st.write("**🔧 TROUBLESHOOTING — If SSH from guest fails:**")

st.write("On the **guest**, run SSH with verbose output:")
st.code("ssh -vvv -i ~/testuser_key testuser@HOST_IP", language="bash")

st.write("On the **host**, check sshd logs:")
st.code("sudo journalctl -u sshd -e", language="bash")

st.write("On the **host**, check all permissions:")
st.code("sudo stat -c '%a %U:%G %n' /home/visitors/testuser", language="bash")
st.code("sudo stat -c '%a %U:%G %n' /home/visitors/testuser/.ssh", language="bash")
st.code("sudo stat -c '%a %U:%G %n' /home/visitors/testuser/.ssh/authorized_keys", language="bash")

st.info("""Expected:
`700 testuser:testuser /home/visitors/testuser`
`700 testuser:testuser /home/visitors/testuser/.ssh`
`600 testuser:testuser /home/visitors/testuser/.ssh/authorized_keys`""")

st.write("If permissions are wrong, fix them on the **host**:")
st.code("sudo chown testuser:testuser /home/visitors/testuser", language="bash")
st.code("sudo chmod 700 /home/visitors/testuser", language="bash")
st.code("sudo chown testuser:testuser /home/visitors/testuser/.ssh", language="bash")
st.code("sudo chmod 700 /home/visitors/testuser/.ssh", language="bash")
st.code("sudo chown testuser:testuser /home/visitors/testuser/.ssh/authorized_keys", language="bash")
st.code("sudo chmod 600 /home/visitors/testuser/.ssh/authorized_keys", language="bash")
st.code("sudo systemctl restart sshd", language="bash")

st.divider()

# ════════════════════════════════════════════════════════════════
# GUEST VM SETUP
# ════════════════════════════════════════════════════════════════

st.subheader("═══ GUEST VM SETUP ═══")

st.divider()

# ════════════════════════════════════════════
# STEP 18
# ════════════════════════════════════════════
st.header("Step 18: Set Up Guest VM")
st.write("The assignment requires users on **both host and guest**. Copy the scripts from the host to the guest.")
st.write("")
st.write("From the **host** as **user0**:")
st.code("scp ~/visitors/* user0@GUEST_IP:~/visitors/", language="bash")
st.warning("⚠️ Replace `GUEST_IP` with your QEMU guest's IP.")

st.write("If scp doesn't work, you can also SSH to the guest and manually re-run steps 2–7 there.")
st.write("")
st.write("Then on the **guest**, run the same setup. If the guest has a GUI with paste, paste these. Otherwise type or SSH into the guest from the host and paste:")
st.code("sudo pacman -S --needed wget openssh zsh", language="bash")
st.code("sudo ssh-keygen -A", language="bash")
st.code("sudo systemctl enable sshd", language="bash")
st.code("sudo systemctl start sshd", language="bash")
st.code("sudo sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config", language="bash")
st.code("sudo systemctl restart sshd", language="bash")
st.code("cd ~/visitors", language="bash")
st.code("sudo bash ~/visitors/add_visitors.sh ~/visitors/newusers.txt https://www.cs.fsu.edu/~langley/NEWKEYS/", language="bash")

st.write("Install testuser key on guest too:")
st.code("sudo cp ~/testkeys/testuser_key.pub /home/visitors/testuser/.ssh/authorized_keys", language="bash")
st.code("sudo chown testuser:testuser /home/visitors/testuser/.ssh/authorized_keys", language="bash")
st.code("sudo chmod 600 /home/visitors/testuser/.ssh/authorized_keys", language="bash")

st.write("Verify on guest:")
st.code("sudo bash ~/visitors/verify_users.sh ~/visitors/newusers.txt", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 19
# ════════════════════════════════════════════
st.header("Step 19: Cleanup (If You Need to Redo)")
st.write("If something went wrong, clean up and start fresh. As **user0**:")
st.code("sudo bash ~/visitors/remove_visitors.sh ~/visitors/newusers.txt", language="bash")
st.write("Then go back to **Step 12** and re-run.")

st.divider()
st.caption("CNT4603 Spring 2026 — Visitor Setup Guide | Arch Linux | QEMU Lab Environment")
