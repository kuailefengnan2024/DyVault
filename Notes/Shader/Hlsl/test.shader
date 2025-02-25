float fit(float value, float a, float b)
{
    return a + (b - a) * value;
}


float test = 2;
float result = fit(test, 0, 1);
printf("Result: %f\n", result);
return result;
