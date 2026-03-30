import streamlit as st

st.set_page_config(page_title="CNT4603 Visitor Setup Guide", page_icon="🐧", layout="wide")

st.title("$ add_visitors.sh")
st.caption("CNT4603 — Understanding Passwords, Accounts & SSH | Arch Linux")

st.sidebar.header("Navigation")
st.sidebar.markdown("""
- [Step 0: Prerequisites](#step-0-prerequisites)
- [Step 1: Create newusers.txt](#step-1-create-newusers-txt)
- [Step 2: Create add_visitors.sh](#step-2-create-add-visitors-sh)
- [Step 3: Create setup_testuser.sh](#step-3-create-setup-testuser-sh)
- [Step 4: Create verify_users.sh](#step-4-create-verify-users-sh)
- [Step 5: Create remove_visitors.sh](#step-5-create-remove-visitors-sh)
- [Step 6: Generate Test Keypair](#step-6-generate-test-keypair)
- [Step 7: Run Main Script](#step-7-run-main-script)
- [Step 8: Install Test Key](#step-8-install-test-key)
- [Step 9: Configure sshd](#step-9-configure-sshd-arch-specific)
- [Step 10: Test SSH Login](#step-10-test-ssh-login)
- [Step 11: Verify Everything](#step-11-verify-everything)
- [Step 12: Repeat on Guest](#step-12-repeat-on-guest-machine)
- [Step 13: Cleanup](#step-13-cleanup-if-you-need-to-redo)
""")

# ════════════════════════════════════════════
# STEP 0
# ════════════════════════════════════════════
st.header("Step 0: Prerequisites")
st.write("Log in as **root** on your Arch machine. Create a working directory and install deps:")
st.code("""mkdir -p /root/visitors
cd /root/visitors
pacman -S --needed wget openssh zsh""", language="bash")
st.info("Run every step from `/root/visitors/` unless noted otherwise.")

# ════════════════════════════════════════════
# STEP 1
# ════════════════════════════════════════════
st.header("Step 1: Create newusers.txt")
st.write("All 68 real users + **testuser** (uid 5099). Format: `username:uid:GECOS:shell`")
st.code("""cat > newusers.txt << 'EOF'
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

# ════════════════════════════════════════════
# STEP 2
# ════════════════════════════════════════════
st.header("Step 2: Create add_visitors.sh")
st.write("The **main script**. Creates users, groups, home dirs under `/home/visitors/`, downloads pubkeys, sets SSH perms, creates `/scratch/` dirs.")
st.code(r"""cat > add_visitors.sh << 'SCRIPTEOF'
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
SCRIPTEOF
chmod +x add_visitors.sh""", language="bash")

# ════════════════════════════════════════════
# STEP 3
# ════════════════════════════════════════════
st.header("Step 3: Create setup_testuser.sh")
st.warning("⚠️ Run this as your **normal user** (user0 or user1), NOT as root.")
st.code(r"""cat > setup_testuser.sh << 'SCRIPTEOF'
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
SCRIPTEOF
chmod +x setup_testuser.sh""", language="bash")

# ════════════════════════════════════════════
# STEP 4
# ════════════════════════════════════════════
st.header("Step 4: Create verify_users.sh")
st.write("Checks uid, gid, home perms, `.ssh` perms, `authorized_keys`, and `/scratch` dir for every user.")
st.code(r"""cat > verify_users.sh << 'SCRIPTEOF'
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
SCRIPTEOF
chmod +x verify_users.sh""", language="bash")

# ════════════════════════════════════════════
# STEP 5
# ════════════════════════════════════════════
st.header("Step 5: Create remove_visitors.sh")
st.write("Cleanup script if you need to redo everything.")
st.code(r"""cat > remove_visitors.sh << 'SCRIPTEOF'
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
SCRIPTEOF
chmod +x remove_visitors.sh""", language="bash")

# ════════════════════════════════════════════
# STEP 6
# ════════════════════════════════════════════
st.header("Step 6: Generate Test Keypair")
st.warning("⚠️ Switch to **user0** or **user1** for this step. NOT root.")
st.code("""cd /root/visitors
bash setup_testuser.sh""", language="bash")
st.write("This creates `~/testkeys/testuser_key` (private) and `testuser_key.pub` (public).")

# ════════════════════════════════════════════
# STEP 7
# ════════════════════════════════════════════
st.header("Step 7: Run Main Script")
st.error("🔴 Run as **root**. This creates all 69 users.")
st.code("""cd /root/visitors
bash add_visitors.sh newusers.txt https://www.cs.fsu.edu/~langley/NEWKEYS/""", language="bash")
st.write("Watch output: **SUCCESS** = pubkey found, **NOTICE** = no pubkey (both are expected per the assignment).")

# ════════════════════════════════════════════
# STEP 8
# ════════════════════════════════════════════
st.header("Step 8: Install Test Key")
st.write("`testuser.pub` doesn't exist on the server, so install the key you made in step 6:")
st.code("""# Change user0 to user1 if that's your normal account
sudo cp /home/user0/testkeys/testuser_key.pub /home/visitors/testuser/.ssh/authorized_keys
sudo chown testuser:testuser /home/visitors/testuser/.ssh/authorized_keys
sudo chmod 600 /home/visitors/testuser/.ssh/authorized_keys""", language="bash")
st.info("If your normal user is **user1**, change `/home/user0/` to `/home/user1/` above.")

# ════════════════════════════════════════════
# STEP 9
# ════════════════════════════════════════════
st.header("Step 9: Configure sshd (Arch-Specific)")
st.code("""# Generate host keys (Arch requirement)
ssh-keygen -A

# Enable PubkeyAuthentication
sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Verify it's set
grep -i "PubkeyAuthentication" /etc/ssh/sshd_config

# Enable and restart sshd
systemctl enable sshd
systemctl restart sshd""", language="bash")
st.warning("If `grep` shows nothing, add it manually: `echo \"PubkeyAuthentication yes\" >> /etc/ssh/sshd_config` then restart sshd.")

# ════════════════════════════════════════════
# STEP 10
# ════════════════════════════════════════════
st.header("Step 10: Test SSH Login")
st.info("Switch to **user0/user1** for this test.")
st.code("""# SSH in with the private key
ssh -i ~/testkeys/testuser_key testuser@localhost

# Once logged in, verify:
whoami
id
pwd
ls -la ~
ls -la ~/.ssh
ls -la /scratch/testuser

# Exit
exit""", language="bash")
st.success("✅ If you get a shell as **testuser** without a password prompt, pubkey auth is working!")

st.write("**If it fails:**")
st.write("""
- Debug: `ssh -vvv -i ~/testkeys/testuser_key testuser@localhost`
- Check logs: `journalctl -u sshd -e`
- Verify: home=700, .ssh=700, authorized_keys=600, all owned by testuser:testuser
- Make sure `/home/visitors/testuser` is NOT world-writable or group-writable
""")

# ════════════════════════════════════════════
# STEP 11
# ════════════════════════════════════════════
st.header("Step 11: Verify Everything")
st.code("""cd /root/visitors
bash verify_users.sh newusers.txt""", language="bash")
st.write("All **OK** = good. **WARN: ak empty** = expected for users who didn't provide a pubkey.")

# ════════════════════════════════════════════
# STEP 12
# ════════════════════════════════════════════
st.header("Step 12: Repeat on Guest Machine")
st.write("The assignment requires both **host and guest**. Copy scripts to the guest and repeat steps 7–11:")
st.code("""# Copy to guest (adjust IP/port for your setup)
scp /root/visitors/* root@GUEST_IP:/root/visitors/

# SSH to guest, then run steps 7-11 again""", language="bash")

# ════════════════════════════════════════════
# STEP 13
# ════════════════════════════════════════════
st.header("Step 13: Cleanup (If You Need to Redo)")
st.code("""cd /root/visitors
bash remove_visitors.sh newusers.txt
# Then re-run from Step 7""", language="bash")

st.divider()
st.caption("CNT4603 Spring 2026 — Visitor Setup Guide")
