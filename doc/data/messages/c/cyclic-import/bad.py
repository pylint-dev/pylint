cat > a.py <<EOF
import b

EOF

cat > b.py <<EOF
import a

EOF
