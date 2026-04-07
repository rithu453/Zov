from fastapi import Header, HTTPException, status

def get_current_role(x_role: str = Header(...)):
    # expects header: x-role: admin / analyst / viewer
    return x_role


def role_required(allowed_roles: list):
    def check(role: str = Header(...)):
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Denied"
            )
        return role
    return check