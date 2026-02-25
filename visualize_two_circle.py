import math
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from two_circle_josephus import two_circle_josephus


# ----------------------------
# Circle Layout Helper
# ----------------------------
def circle_positions(n, center, radius):
    if n == 0:
        return []
    cx, cy = center
    positions = []
    for i in range(n):
        angle = (math.pi / 2) - (2 * math.pi * i / n)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        positions.append((x, y))
    return positions


# ----------------------------
# Draw One Circle
# ----------------------------
def draw_circle(ax, people, center, radius, label, active):
    outline = plt.Circle(center, radius, fill=False, linewidth=3 if active else 1.5)
    ax.add_patch(outline)

    cx, cy = center
    ax.text(cx, cy + radius + 0.35,
            label + (" (TURN)" if active else ""),
            ha="center", va="center", fontsize=12)

    if not people:
        ax.text(cx, cy, "(empty)", ha="center", va="center")
        return

    positions = circle_positions(len(people), center, radius)

    for i, person in enumerate(people):
        x, y = positions[i]
        is_pointer = (i == 0)

        ax.scatter(x, y, s=250 if is_pointer else 150)
        ax.text(x, y, str(person), ha="center", va="center", color="white")

        if is_pointer:
            ax.scatter(x, y, s=450, facecolors="none", linewidths=2)


# ----------------------------
# Trace Player Class
# ----------------------------
class TracePlayer:
    def __init__(self, steps):
        self.steps = steps
        self.index = 0

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        # Leave space for buttons
        plt.subplots_adjust(bottom=0.15)

        # --- Buttons ---
        ax_prev = self.fig.add_axes([0.30, 0.03, 0.12, 0.06])
        ax_next = self.fig.add_axes([0.44, 0.03, 0.12, 0.06])
        ax_reset = self.fig.add_axes([0.58, 0.03, 0.12, 0.06])

        self.btn_prev = Button(ax_prev, "Prev")
        self.btn_next = Button(ax_next, "Next")
        self.btn_reset = Button(ax_reset, "Reset")

        self.btn_prev.on_clicked(self.prev_step)
        self.btn_next.on_clicked(self.next_step)
        self.btn_reset.on_clicked(self.reset)

        self.draw()

    def next_step(self, _event=None):
        self.index = min(self.index + 1, len(self.steps) - 1)
        self.draw()

    def prev_step(self, _event=None):
        self.index = max(self.index - 1, 0)
        self.draw()

    def reset(self, _event=None):
        self.index = 0
        self.draw()

    def draw(self):
        self.ax.clear()
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        step = self.steps[self.index]
        turn = step.get("turn", "?")
        eliminated = step.get("eliminated", None)
        phase = step.get("phase", "main")
        A = step.get("A", [])
        B = step.get("B", [])

        status = f"Step {self.index+1}/{len(self.steps)} | Phase: {phase} | Turn: {turn} | Eliminated: {eliminated}"
        self.ax.text(0.5, 0.97, status,
                     transform=self.ax.transAxes,
                     ha="center", va="center", fontsize=13)

        draw_circle(self.ax, A, (-2.2, 0.0), 1.2,
                    f"Circle A (size={len(A)})", active=(turn == "A"))
        draw_circle(self.ax, B, (2.2, 0.0), 1.2,
                    f"Circle B (size={len(B)})", active=(turn == "B"))

        self.ax.set_xlim(-4, 4)
        self.ax.set_ylim(-2.6, 2.6)

        self.fig.canvas.draw_idle()

# ----------------------------
# Main Runner
# ----------------------------
def main():
    n = 10
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    winner, steps = two_circle_josephus(n, trace=True)

    print(f"Winner for n={n}: {winner}")

    TracePlayer(steps)
    plt.show()


if __name__ == "__main__":
    main()