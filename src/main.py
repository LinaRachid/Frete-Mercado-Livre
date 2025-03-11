import re
import asyncio
import aiohttp
from typing import Optional, List
import tkinter as tk
from tkinter import scrolledtext, messagebox

def normalize_ad_id(ad_id: str) -> Optional[str]:
    """Normalize a Mercado Livre ad ID to 'MLB' + digits format."""
    cleaned_id = re.sub(r"[^MLB0-9]", "", ad_id.strip())
    if not cleaned_id.startswith("MLB"):
        cleaned_id = "MLB" + cleaned_id
    return cleaned_id if re.match(r"^MLB\d+$", cleaned_id) else None

def normalize_zip_code(zip_code: str) -> Optional[str]:
    """Normalize a Brazilian ZIP code to 8 digits."""
    cleaned_zip = re.sub(r"[^0-9]", "", zip_code.strip())
    return cleaned_zip if len(cleaned_zip) == 8 and cleaned_zip.isdigit() else None

async def fetch_shipping_cost(session: aiohttp.ClientSession, ad_id: str, zip_code: str) -> tuple[str, Optional[float], Optional[str]]:
    """Fetch the shipping cost for a single ad ID."""
    url = f"https://api.mercadolibre.com/items/{ad_id}/shipping_options?zip_code={zip_code}"
    headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
            response.raise_for_status()
            data = await response.json()
            if "options" in data and len(data["options"]) > 2:
                return ad_id, float(data["options"][2]["list_cost"]), None
            return ad_id, None, "No shipping options available"
    except aiohttp.ClientConnectionError as error:
        return ad_id, None, f"Could not connect to the server. Please check your internet connection and try again."
    except aiohttp.ClientResponseError as error:
        if error.status == 500:
            return ad_id, None, f"Server error (500). The Mercado Livre API is experiencing issues. Please try again later."
        elif error.status == 404:
            return ad_id, None, f"Item not found (404). Verify the ad ID and try again."
        elif error.status == 429:
            return ad_id, None, f"Too many requests (429). Please wait a few minutes and try again."
        else:
            return ad_id, None, f"Unexpected HTTP error ({error.status}). Contact the developer if this persists."
    except aiohttp.ClientError as error:
        return ad_id, None, f"Client error: {error}. Check your connection or contact the developer."
    except ValueError as error:
        return ad_id, None, f"Invalid response: {error}. The API returned unexpected data. Try again or contact the developer."
    except Exception as error:
        return ad_id, None, f"Unexpected error: {error}. Please contact the developer with this error message."

async def process_ad_ids(ad_ids: str, zip_code: str, result_text: scrolledtext.ScrolledText) -> None:
    """Process multiple ad IDs asynchronously and display results in order."""
    id_list = list(dict.fromkeys([id.strip() for id in re.split(r"[,\n]", ad_ids) if id.strip()]))
    if not id_list:
        return
    
    normalized_ids = [(raw_id, normalize_ad_id(raw_id)) for raw_id in id_list]
    valid_ids = [(raw_id, norm_id) for raw_id, norm_id in normalized_ids if norm_id]
    invalid_ids = [(raw_id, None) for raw_id, norm_id in normalized_ids if not norm_id]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_shipping_cost(session, norm_id, zip_code) for _, norm_id in valid_ids]
        results = await asyncio.gather(*tasks)
    
    result_dict = {ad_id: (cost, error) for ad_id, cost, error in results}
    
    for raw_id, norm_id in normalized_ids:
        if norm_id:
            cost, error = result_dict.get(norm_id, (None, "Unknown error"))
            if cost is not None:
                result_text.insert(tk.END, f"{norm_id}: R$ {cost:.2f}\n")
            else:
                result_text.insert(tk.END, f"{norm_id}: Failed to retrieve cost\n")
                messagebox.showerror("Error", error)
        else:
            result_text.insert(tk.END, f"Skipping invalid ad ID: {raw_id}\n")
            messagebox.showwarning("Warning", f"Invalid ad ID: {raw_id}. Must be in the format MLB followed by numbers.")
        result_text.see(tk.END)

def run_gui():
    """Launch a simple GUI for the shipping cost extractor."""
    def calculate_shipping():
        ad_ids = ad_id_entry.get("1.0", tk.END).strip()
        zip_code = zip_entry.get().strip()
        
        normalized_zip = normalize_zip_code(zip_code)
        if not normalized_zip:
            messagebox.showerror("Error", "Invalid ZIP code. Must be 8 digits (e.g., 01001000).")
            return
        
        if not ad_ids:
            messagebox.showerror("Error", "Please enter at least one ad ID.")
            return
        
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "⚠️ This tool extracts shipping costs only for Mercado Livre listings, not Mercado Shops.\n")
        result_text.insert(tk.END, "Fetching shipping costs...\n")
        window.update()
        
        def run_async():
            asyncio.run(process_ad_ids(ad_ids, normalized_zip, result_text))
        
        window.after(0, run_async)

    def show_contact_info():
        messagebox.showinfo("Contact the Developer", "For bugs, errors, suggestions, or inquiries, contact me:\n- GitHub: LinaRachid\n- X: @SEU_USUARIO\n- Email: seu.email@example.com")

    window = tk.Tk()
    window.title("Mercado Livre Shipping Extractor")
    window.geometry("400x500")
    window.resizable(True, True)
    
    tk.Label(window, text="Ad IDs (one per line or comma-separated):").pack(pady=5)
    ad_id_entry = scrolledtext.ScrolledText(window, height=10, width=40)
    ad_id_entry.pack(pady=5, fill=tk.BOTH, expand=True)
    
    tk.Label(window, text="Sender ZIP Code (e.g., 01001000 or 01.001-000):").pack(pady=5)
    zip_entry = tk.Entry(window, width=20)
    zip_entry.pack(pady=5)
    
    tk.Button(window, text="Calculate Shipping", command=calculate_shipping).pack(pady=10)
    
    tk.Label(window, text="Results:").pack(pady=5)
    result_text = scrolledtext.ScrolledText(window, height=10, width=40)
    result_text.pack(pady=5, fill=tk.BOTH, expand=True)
    
    tk.Button(window, text="Contact Developer", command=show_contact_info).pack(pady=5)
    
    window.mainloop()

if __name__ == "__main__":
    run_gui()