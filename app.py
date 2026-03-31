import streamlit as st

st.set_page_config(page_title="CNT4603 Visitor Setup Guide", page_icon="🐧", layout="wide")

st.title("🐧 CNT4603 Visitor Setup — Complete Arch Linux Guide")
st.caption("Every command you need, in order. Just copy and paste into your Arch terminal.")

st.sidebar.header("📋 All Steps")
st.sidebar.markdown("""
- [Step 0: Install Dependencies](#step-0-install-dependencies)
- [Step 1: Create Working Directory](#step-1-create-working-directory)
- [Step 2: Create newusers.txt](#step-2-create-newusers-txt)
- [Step 3: Create add_visitors.sh](#step-3-create-add-visitors-sh)
- [Step 4: Create setup_testuser.sh](#step-4-create-setup-testuser-sh)
- [Step 5: Create verify_users.sh](#step-5-create-verify-users-sh)
- [Step 6: Create remove_visitors.sh](#step-6-create-remove-visitors-sh)
- [Step 7: Make Scripts Executable](#step-7-make-all-scripts-executable)
- [Step 8: Generate SSH Host Keys](#step-8-generate-ssh-host-keys-arch-requirement)
- [Step 9: Enable sshd Service](#step-9-enable-and-start-sshd)
- [Step 10: Configure sshd_config](#step-10-configure-sshd-config)
- [Step 11: Restart sshd](#step-11-restart-sshd)
- [Step 12: Generate Test Keypair](#step-12-generate-test-keypair)
- [Step 13: Run Main Script](#step-13-run-the-main-script)
- [Step 14: Install Test Key](#step-14-install-testuser-key)
- [Step 15: Test SSH Login](#step-15-test-ssh-login)
- [Step 16: Verify All Users](#step-16-verify-all-users)
- [Step 17: Repeat on Guest](#step-17-repeat-on-guest-machine)
- [Step 18: Cleanup (if needed)](#step-18-cleanup-if-you-need-to-redo)
""")

st.divider()

# ════════════════════════════════════════════
# STEP 0
# ════════════════════════════════════════════
st.header("Step 0: Install Dependencies")
st.write("Log in as **root** on your Arch machine and run:")
st.code("pacman -Syu", language="bash")
st.code("pacman -S --needed wget openssh zsh", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 1
# ════════════════════════════════════════════
st.header("Step 1: Create Working Directory")
st.code("mkdir -p /root/visitors", language="bash")
st.code("cd /root/visitors", language="bash")
st.warning("⚠️ Run **ALL** remaining steps from inside `/root/visitors/`")

st.divider()

# ════════════════════════════════════════════
# STEP 2
# ════════════════════════════════════════════
st.header("Step 2: Create newusers.txt")
st.write("This creates the file with all 68 real users + testuser (uid 5099):")
st.code("""cat > /root/visitors/newusers.txt << 'EOF'
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
st.code("cat /root/visitors/newusers.txt", language="bash")
st.code("wc -l /root/visitors/newusers.txt", language="bash")
st.info("You should see **69 lines** (68 real users + 1 testuser).")

st.divider()

# ════════════════════════════════════════════
# STEP 3
# ════════════════════════════════════════════
st.header("Step 3: Create add_visitors.sh")
st.write("This is the **main script**. It creates users, groups, home dirs under `/home/visitors/`, downloads pubkeys, sets SSH perms, and creates `/scratch/` dirs.")
st.code(r"""cat > /root/visitors/add_visitors.sh << 'SCRIPTEOF'
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

# Arch: generate SSH host keys if missing
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

    # Create group (gid == uid)
    groupadd -g "$uid" "$name"

    # Create user with home under /home/visitors/
    useradd \
        -u "$uid" \
        -g "$name" \
        -d "$HOMEDIR" \
        -m \
        -k /etc/skel \
        -s "$shell" \
        -c "$gecos" \
        "$name"

    # Lock password
    passwd -l "$name" 2>/dev/null || true

    # Home dir perms (SSH needs 700, owned by user)
    chown "$name":"$name" "$HOMEDIR"
    chmod 700 "$HOMEDIR"

    # .ssh dir (SSH needs 700, owned by user)
    mkdir -p "${HOMEDIR}/.ssh"
    chown "$name":"$name" "${HOMEDIR}/.ssh"
    chmod 700 "${HOMEDIR}/.ssh"

    # Download pubkey
    PUBKEY_FILE="${PUBKEY_URL}${name}.pub"
    echo "  Fetching: $PUBKEY_FILE"
    if wget -q -O "${HOMEDIR}/.ssh/authorized_keys" "$PUBKEY_FILE" 2>/dev/null; then
        echo "  SUCCESS: Pubkey installed."
    else
        echo "  NOTICE: No pubkey for $name."
        touch "${HOMEDIR}/.ssh/authorized_keys"
    fi

    # authorized_keys perms (SSH needs 600, owned by user)
    chown "$name":"$name" "${HOMEDIR}/.ssh/authorized_keys"
    chmod 600 "${HOMEDIR}/.ssh/authorized_keys"

    # /scratch dir
    mkdir -p "$SCRATCHDIR"
    chown "$name":"$name" "$SCRATCHDIR"
    chmod 700 "$SCRATCHDIR"

    echo "  Done: $name"
    echo ""
done < "$USERFILE"

echo "============================================"
echo "ALL USERS PROCESSED."
echo "============================================"
echo "Permissions set:"
echo "  /home/visitors/USER/                 -> 700 user:user"
echo "  /home/visitors/USER/.ssh/            -> 700 user:user"
echo "  /home/visitors/USER/.ssh/authorized_keys -> 600 user:user"
echo "  /scratch/USER/                       -> 700 user:user"
SCRIPTEOF""", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 4
# ════════════════════════════════════════════
st.header("Step 4: Create setup_testuser.sh")
st.write("This script generates an SSH keypair for testuser so you have the private key to test login.")
st.code(r"""cat > /root/visitors/setup_testuser.sh << 'SCRIPTEOF'
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
echo ""
echo "After add_visitors.sh, install key with:"
echo "  sudo cp ${KEYDIR}/testuser_key.pub /home/visitors/testuser/.ssh/authorized_keys"
echo "  sudo chown testuser:testuser /home/visitors/testuser/.ssh/authorized_keys"
echo "  sudo chmod 600 /home/visitors/testuser/.ssh/authorized_keys"
echo ""
echo "Then test: ssh -i ${KEYDIR}/testuser_key testuser@localhost"
SCRIPTEOF""", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 5
# ════════════════════════════════════════════
st.header("Step 5: Create verify_users.sh")
st.write("This checks every user's uid, gid, home dir permissions, `.ssh` permissions, `authorized_keys`, and `/scratch` dir.")
st.code(r"""cat > /root/visitors/verify_users.sh << 'SCRIPTEOF'
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
st.write("Cleanup script in case you need to start over.")
st.code(r"""cat > /root/visitors/remove_visitors.sh << 'SCRIPTEOF'
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
st.code("""chmod +x /root/visitors/add_visitors.sh
chmod +x /root/visitors/setup_testuser.sh
chmod +x /root/visitors/verify_users.sh
chmod +x /root/visitors/remove_visitors.sh""", language="bash")

st.write("Verify they are all there:")
st.code("ls -la /root/visitors/", language="bash")
st.info("You should see: `add_visitors.sh`, `setup_testuser.sh`, `verify_users.sh`, `remove_visitors.sh`, and `newusers.txt`")

st.divider()

# ════════════════════════════════════════════
# STEP 8
# ════════════════════════════════════════════
st.header("Step 8: Generate SSH Host Keys (Arch Requirement)")
st.error("🔴 This is **required on Arch Linux** before sshd works. Run as root:")
st.code("ssh-keygen -A", language="bash")

st.write("Verify keys were created:")
st.code("ls -la /etc/ssh/ssh_host_*", language="bash")
st.info("You should see several key files like `ssh_host_rsa_key`, `ssh_host_ed25519_key`, etc.")

st.divider()

# ════════════════════════════════════════════
# STEP 9
# ════════════════════════════════════════════
st.header("Step 9: Enable and Start sshd")
st.code("systemctl enable sshd", language="bash")
st.code("systemctl start sshd", language="bash")

st.write("Check it's running:")
st.code("systemctl status sshd", language="bash")
st.success("You should see **active (running)** in green.")

st.divider()

# ════════════════════════════════════════════
# STEP 10
# ════════════════════════════════════════════
st.header("Step 10: Configure sshd_config")
st.write("Make sure PubkeyAuthentication is enabled:")
st.code("grep -i 'PubkeyAuthentication' /etc/ssh/sshd_config", language="bash")

st.write("If it shows `#PubkeyAuthentication yes` or `PubkeyAuthentication no` or nothing, fix it:")
st.code("sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config", language="bash")

st.write("If grep showed **nothing at all**, add it:")
st.code('echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config', language="bash")

st.write("Verify the fix:")
st.code("grep -i 'PubkeyAuthentication' /etc/ssh/sshd_config", language="bash")
st.success("You should see: `PubkeyAuthentication yes`")

st.divider()

# ════════════════════════════════════════════
# STEP 11
# ════════════════════════════════════════════
st.header("Step 11: Restart sshd")
st.write("Apply the config changes:")
st.code("systemctl restart sshd", language="bash")

st.write("Confirm it's still running:")
st.code("systemctl status sshd", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 12
# ════════════════════════════════════════════
st.header("Step 12: Generate Test Keypair")
st.warning("⚠️ **Switch to your normal user (user0 or user1) for this step. NOT root.**")

st.write("If you are root, switch user first:")
st.code("su - user0", language="bash")

st.write("Then run the setup script:")
st.code("bash /root/visitors/setup_testuser.sh", language="bash")

st.write("If you get a **permission denied** error, copy the script first:")
st.code("""cp /root/visitors/setup_testuser.sh /tmp/
bash /tmp/setup_testuser.sh""", language="bash")

st.info("This creates `~/testkeys/testuser_key` (private) and `~/testkeys/testuser_key.pub` (public). **Remember which user you ran this as** — you need the path in step 14.")

st.write("Switch back to root when done:")
st.code("exit", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 13
# ════════════════════════════════════════════
st.header("Step 13: Run the Main Script")
st.error("🔴 Run as **root**. This creates all 69 user accounts.")
st.code("cd /root/visitors", language="bash")
st.code("bash add_visitors.sh newusers.txt https://www.cs.fsu.edu/~langley/NEWKEYS/", language="bash")

st.write("This will take a minute. Watch the output:")
st.write("- **SUCCESS: Pubkey installed** = user had a pubkey on the server")
st.write("- **NOTICE: No pubkey for X** = user didn't provide one (expected per assignment)")

st.write("When done, spot-check a few users:")
st.code("id adams", language="bash")
st.code("id turing", language="bash")
st.code("id testuser", language="bash")
st.code("ls -la /home/visitors/adams/", language="bash")
st.code("ls -la /home/visitors/adams/.ssh/", language="bash")
st.code("ls -la /scratch/adams/", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 14
# ════════════════════════════════════════════
st.header("Step 14: Install testuser Key")
st.write("Since `testuser.pub` doesn't exist on the professor's server, manually install the key you generated in step 12.")

st.write("**If you ran setup_testuser.sh as user0:**")
st.code("""cp /home/user0/testkeys/testuser_key.pub /home/visitors/testuser/.ssh/authorized_keys
chown testuser:testuser /home/visitors/testuser/.ssh/authorized_keys
chmod 600 /home/visitors/testuser/.ssh/authorized_keys""", language="bash")

st.write("**If you ran setup_testuser.sh as user1:**")
st.code("""cp /home/user1/testkeys/testuser_key.pub /home/visitors/testuser/.ssh/authorized_keys
chown testuser:testuser /home/visitors/testuser/.ssh/authorized_keys
chmod 600 /home/visitors/testuser/.ssh/authorized_keys""", language="bash")

st.write("Verify the key is installed:")
st.code("cat /home/visitors/testuser/.ssh/authorized_keys", language="bash")
st.code("stat -c '%a %U:%G' /home/visitors/testuser/.ssh/authorized_keys", language="bash")
st.success("Should show: `600 testuser:testuser`")

st.divider()

# ════════════════════════════════════════════
# STEP 15
# ════════════════════════════════════════════
st.header("Step 15: Test SSH Login")
st.warning("⚠️ **Switch to your normal user (user0 or user1) — whichever one has the private key.**")

st.code("su - user0", language="bash")

st.write("SSH into testuser using the private key:")
st.code("ssh -i ~/testkeys/testuser_key testuser@localhost", language="bash")

st.write("If it asks about the host fingerprint, type **yes** and press Enter.")
st.write("")
st.write("Once logged in, run these commands to verify everything:")
st.code("whoami", language="bash")
st.code("id", language="bash")
st.code("pwd", language="bash")
st.code("ls -la ~", language="bash")
st.code("ls -la ~/.ssh", language="bash")
st.code("ls -la ~/.ssh/authorized_keys", language="bash")
st.code("ls -la /scratch/testuser", language="bash")

st.success("✅ If you got a shell as `testuser` **without being asked for a password**, SSH pubkey auth is working!")

st.write("Exit the testuser session:")
st.code("exit", language="bash")

st.write("Exit back to root:")
st.code("exit", language="bash")

st.write("---")
st.write("**🔧 TROUBLESHOOTING — If SSH login fails:**")

st.write("Run SSH with verbose output:")
st.code("ssh -vvv -i ~/testkeys/testuser_key testuser@localhost", language="bash")

st.write("Check sshd logs:")
st.code("journalctl -u sshd -e", language="bash")

st.write("Check all permissions (as root):")
st.code("""stat -c '%a %U:%G %n' /home/visitors/testuser
stat -c '%a %U:%G %n' /home/visitors/testuser/.ssh
stat -c '%a %U:%G %n' /home/visitors/testuser/.ssh/authorized_keys""", language="bash")
st.info("""Expected output:
`700 testuser:testuser /home/visitors/testuser`
`700 testuser:testuser /home/visitors/testuser/.ssh`
`600 testuser:testuser /home/visitors/testuser/.ssh/authorized_keys`""")

st.write("If permissions are wrong, fix them:")
st.code("""chown testuser:testuser /home/visitors/testuser
chmod 700 /home/visitors/testuser
chown testuser:testuser /home/visitors/testuser/.ssh
chmod 700 /home/visitors/testuser/.ssh
chown testuser:testuser /home/visitors/testuser/.ssh/authorized_keys
chmod 600 /home/visitors/testuser/.ssh/authorized_keys""", language="bash")

st.write("Then restart sshd and try again:")
st.code("systemctl restart sshd", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 16
# ════════════════════════════════════════════
st.header("Step 16: Verify All Users")
st.write("Run the verification script as root:")
st.code("cd /root/visitors", language="bash")
st.code("bash verify_users.sh newusers.txt", language="bash")

st.write("What the output means:")
st.write("- **OK** = that check passed")
st.write("- **WARN: ak empty** = user didn't have a pubkey on the server (this is fine)")
st.write("- **FAIL** = something is wrong, fix it")
st.write("- **ALL CHECKS PASSED** at the end = you're done!")

st.divider()

# ════════════════════════════════════════════
# STEP 17
# ════════════════════════════════════════════
st.header("Step 17: Repeat on Guest Machine")
st.write("The assignment requires users on **both host and guest**. Copy everything to the guest VM.")

st.write("First, find your guest VM's IP address. On the guest, run:")
st.code("ip addr show", language="bash")

st.write("From the **host**, copy all scripts to the guest:")
st.code("scp /root/visitors/* root@GUEST_IP:/root/visitors/", language="bash")
st.warning("⚠️ Replace `GUEST_IP` with your actual guest VM IP address.")

st.write("SSH into the guest:")
st.code("ssh root@GUEST_IP", language="bash")

st.write("Then on the guest, repeat these steps:")
st.code("""cd /root/visitors

# Install deps
pacman -S --needed wget openssh zsh

# Host keys
ssh-keygen -A

# Enable sshd
systemctl enable sshd
systemctl start sshd

# Config
sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd

# Run main script
bash add_visitors.sh newusers.txt https://www.cs.fsu.edu/~langley/NEWKEYS/

# Install test key (adjust user0/user1 path)
cp /home/user0/testkeys/testuser_key.pub /home/visitors/testuser/.ssh/authorized_keys
chown testuser:testuser /home/visitors/testuser/.ssh/authorized_keys
chmod 600 /home/visitors/testuser/.ssh/authorized_keys

# Verify
bash verify_users.sh newusers.txt""", language="bash")

st.divider()

# ════════════════════════════════════════════
# STEP 18
# ════════════════════════════════════════════
st.header("Step 18: Cleanup (If You Need to Redo)")
st.write("If something went wrong and you need to start fresh, run as root:")
st.code("cd /root/visitors", language="bash")
st.code("bash remove_visitors.sh newusers.txt", language="bash")

st.write("This removes all users, groups, home dirs, and scratch dirs. Then go back to **Step 13** and re-run.")

st.divider()
st.caption("CNT4603 Spring 2026 — Visitor Setup Guide | Arch Linux")
