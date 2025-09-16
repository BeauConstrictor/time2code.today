from typing import Iterator, Callable, Any, Tuple
from types import ModuleType
from decimal import Decimal
from pathlib import Path
import sys
import tkinter as tk
from tkinter import ttk

import main


def get_reference(constant: str) -> str:
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys._MEIPASS)  # type: ignore
    else:
        base_dir = Path(__file__).resolve().parent

    file_path = base_dir / "references" / f"{constant}.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def verify_until_mismatch(calculation: str, ref: str) -> Tuple[str, int]:
    matched = []
    correct_digits = 0
    for c_calc, c_ref in zip(calculation, ref):
        if c_calc == c_ref:
            matched.append(c_calc)
            correct_digits += 1
        else:
            break

    if matched and matched[-1] == ".":
        correct_digits -= 1

    return "".join(matched), correct_digits


class IntEntry(tk.Entry):
    def __init__(self, master: tk.Widget, allow_negative: bool = False, **kwargs: Any) -> None:
        self.allow_negative = allow_negative
        vcmd = (master.register(self._validate), "%P")

        kwargs.update({
            "validate": "key",
            "validatecommand": vcmd
        })

        super().__init__(master, **kwargs)

    def _validate(self, new_value: str) -> bool:
        if new_value == "":
            return True
        if self.allow_negative and new_value == "-":
            return True
        try:
            int(new_value)
            return True
        except ValueError:
            return False

    def get_int(self) -> int | None:
        val = self.get()
        return int(val) if val else None


class SelectionFrame(tk.Frame):
    def __init__(self, master: tk.Widget) -> None:
        super().__init__(master)

        self.selected_const: tk.StringVar = tk.StringVar(value="pi")
        self.selected_const.trace_add("write", self.update_algo_dropdown)

        self.const_dropdown = ttk.Combobox(
            self, textvariable=self.selected_const, values=list(main.modules.keys()), state="readonly"
        )
        self.const_dropdown.grid(row=0, column=0)

        self.selected_algo: tk.StringVar = tk.StringVar()
        self.algo_dropdown = ttk.Combobox(self, textvariable=self.selected_algo, state="readonly")
        self.algo_dropdown.grid(row=0, column=1)
        self.update_algo_dropdown()

        tk.Label(self, text="Digits:").grid(row=0, column=2, padx=(20, 0))
        self.digits_entry = IntEntry(self, allow_negative=False)
        self.digits_entry.grid(row=0, column=3)
        self.digits_entry.insert(0, "100")

        self.begin_btn = tk.Button(self, text="Begin", command=self._dummy_command)
        self.begin_btn.grid(row=0, column=4, padx=(30, 0))

    def _dummy_command(self) -> None:
        pass

    def update_algo_dropdown(self, *_: Any) -> None:
        module = main.modules[self.selected_const.get()]
        algos = list(module.algorithms.keys())
        self.algo_dropdown["values"] = algos
        if algos:
            self.selected_algo.set(algos[0])

    def export(self) -> Tuple[ModuleType, int, Callable[[int], Iterator[Decimal]], int, str]:
        module = main.modules[self.selected_const.get()]
        algo_name = self.selected_algo.get()
        batch_size = module.gui_batch_sizes[algo_name]
        algorithm = module.algorithms[algo_name]
        digits = int(self.digits_entry.get() or 100)
        const = self.selected_const.get()
        self.digits_entry.delete(0, "end")
        self.digits_entry.insert(0, str(digits))
        return module, digits, algorithm, batch_size, const

    def subscribe(self, func: Callable[[Tuple[ModuleType, int, Callable[[int], Iterator[Decimal]], int, str]], Any]) -> None:
        self.begin_btn.config(command=lambda: func(self.export()))


class ProgressBar(ttk.Progressbar):
    def __init__(self, master: tk.Widget) -> None:
        super().__init__(master, orient="horizontal", mode="determinate", length=675)


class OutputBox(tk.Text):
    def __init__(self, root: tk.Tk) -> None:
        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        super().__init__(
            frame,
            wrap="char",
            font=("Courier", 12),
            state="normal",
            height=30,
            width=60,
            bg="white",
            relief="flat",
            borderwidth=0,
            yscrollcommand=scrollbar.set
        )
        self.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.yview)

        self.progress_bar: ProgressBar | None = None
        self.iterator: Iterator[Decimal] | None = None
        self.batch_size: int = 1
        self.root: tk.Tk = root
        self.reference: str = ""

        self.try_convergence()

    def try_convergence(self) -> None:
        if self.iterator:
            try:
                convergence: Decimal | None = None
                for _ in range(self.batch_size):
                    convergence = next(self.iterator)

                if convergence is not None:
                    new_text = str(convergence)
                    output, correct_digits = verify_until_mismatch(new_text, self.reference)

                    self.delete("1.0", "end")
                    self.insert("1.0", output)
                    self.see("end")

                    if self.progress_bar:
                        self.progress_bar["value"] = correct_digits

            except StopIteration:
                self.iterator = None
            except Exception as e:
                self.delete("1.0", "end")
                self.insert("1.0", f"Error: {e}")
                self.iterator = None

        self.root.after(10, self.try_convergence)

    def show_calculation(self, batch_size: int, iterator: Iterator[Decimal], const: str) -> None:
        self.batch_size = batch_size
        self.iterator = iterator
        self.reference = get_reference(const)


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("const-crunch GUI")
        self.resizable(False, False)

        self.selection_frame = SelectionFrame(self)
        self.selection_frame.subscribe(self.start_calculation)
        self.selection_frame.pack()

        self.progress_bar = ProgressBar(self)
        self.progress_bar.pack()

        self.output_box = OutputBox(self)
        self.output_box.progress_bar = self.progress_bar

    def start_calculation(
        self, choices: Tuple[ModuleType, int, Callable[[int], Iterator[Decimal]], int, str]
    ) -> None:
        module, digits, algo, batch_size, const = choices
        self.progress_bar["maximum"] = digits

        try:
            iterator = algo(digits)
        except Exception as e:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("1.0", f"Algorithm error: {e}")
            return

        self.output_box.show_calculation(batch_size, iterator, const)


if __name__ == "__main__":
    print("Starting GUI Directly...")
    app = App()
    app.mainloop()
