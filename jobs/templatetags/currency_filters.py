from django import template

register = template.Library()

@register.filter
def format_zar(value):
    """Format value as South African Rand"""
    if not value:
        return "Salary negotiable"
    
    value = str(value)
    
    # If it already has R, return as is
    if value.startswith('R'):
        return value
    
    # If it has $, convert to R
    if value.startswith('$'):
        return value.replace('$', 'R')
    
    # If it has other currency symbols, add ZAR note
    if any(symbol in value for symbol in ['€', '£', 'USD', 'EUR', 'GBP']):
        return f"R{value} (converted)"
    
    # If no currency symbol, add R
    return f"R{value}"

@register.filter
def format_salary_range(salary_min, salary_max):
    """Format salary range in ZAR"""
    if salary_min and salary_max:
        return f"R{salary_min:,.0f} - R{salary_max:,.0f} per annum"
    elif salary_min:
        return f"From R{salary_min:,.0f} per annum"
    elif salary_max:
        return f"Up to R{salary_max:,.0f} per annum"
    return "Salary negotiable"