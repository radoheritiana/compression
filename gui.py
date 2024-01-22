import tkinter as tk
from tkinter import filedialog, messagebox
from huffman import Huffman
import os


class CompressionDecompressionApp:
    def __init__(self, root):
        self.huffman = Huffman()
        self.root = root
        # Taille fixe de la fenêtre
        self.root.geometry("400x200")
        self.root.title("RHJAR")

        self.label = tk.Label(root, text="Sélectionnez un fichier:")
        self.label.pack(pady=10)

        self.bouton_selection = tk.Button(root, text="Sélectionner un fichier", command=self.selectionner_fichier)
        self.bouton_selection.pack(pady=10)

        self.bouton_compression = tk.Button(root, text="Compression", command=self.compresser)
        self.bouton_compression.pack(pady=10)

        self.bouton_decompression = tk.Button(root, text="Décompression", command=self.decompresser)
        self.bouton_decompression.pack(pady=10)

    def selectionner_fichier(self):
        options = {
            'filetypes': [('Fichiers texte et RHJA', '*.txt;*.rhja')],
        }
        fichier = filedialog.askopenfilename(**options)
        self.fichier = fichier
        self.label.config(text=f"Fichier sélectionné : {fichier}")

    def compresser(self):
        if hasattr(self, 'fichier'):
            if self.fichier.lower().endswith(".txt"):
                fichier_entree = self.fichier
                
                taille_avant = os.path.getsize(fichier_entree)
                
                output = self.huffman.compression(fichier_entree)
                taille_apres = os.path.getsize(output)

                # Calculer le taux de compression
                taux_compression = 100 * (1 - taille_apres / taille_avant)
                taux_compression = "{:.2f}".format(taux_compression)
                messagebox.showinfo("Succès", f"Compression terminée : {output}\n Le taux de compression est de {taux_compression}%")
            else:
                messagebox.showwarning("Avertissement", "Le fichier doit avoir l'extension .txt pour la compression.")
        else:
            messagebox.showwarning("Avertissement", "Aucun fichier sélectionné.")

    def decompresser(self):
        if hasattr(self, 'fichier'):
            if self.fichier.lower().endswith(".rhja"):
                fichier_entree = self.fichier
                taille_avant = os.path.getsize(fichier_entree)
                
                decompressed = self.huffman.decompression(fichier_entree)
                
                taille_apres = os.path.getsize(decompressed)
                # Calculer le taux de décompression
                taux_decompression = 100 * (1 - taille_apres / taille_avant)
                taux_decompression = "{:.2f}".format(taux_decompression)
                messagebox.showinfo("Succès", f"Décompression terminée : {decompressed}\n Le taux de décompression est de {taux_decompression}%")
            else:
                messagebox.showwarning("Avertissement", "Le fichier doit avoir l'extension .rhja pour la décompression.")
        else:
            messagebox.showwarning("Avertissement", "Aucun fichier sélectionné.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompressionDecompressionApp(root)
    root.mainloop()
