import math

def dot_product(vec1, vec2):
    product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    print("Dot product:", product)
    return product

def magnitude(vec):
    mag = math.sqrt(sum(v**2 for v in vec))
    print("Magnitude:", mag)
    return mag

def angle_between(vec1, vec2):
    dot_prod = dot_product(vec1, vec2)
    mag1 = magnitude(vec1)
    mag2 = magnitude(vec2)
    cos_theta = dot_prod / (mag1 * mag2)
    print("Cosine of the angle:", cos_theta)
    angle = math.acos(cos_theta)  # 라디안 단위의 각도
    angle_degrees = math.degrees(angle)  # 각도를 도 단위로 변환
    print("Angle in degrees:", angle_degrees)
    return angle_degrees

if __name__ == "__main__":
    try:
        # 사용자 입력 받기
        vec1 = list(map(float, input("Enter the first vector (comma-separated): ").split(',')))
        vec2 = list(map(float, input("Enter the second vector (comma-separated): ").split(',')))

        result = angle_between(vec1, vec2)
        print("The angle between the vectors is:", result, "degrees")
    except ValueError:
        print("Invalid input. Please enter numeric values separated by commas.")
