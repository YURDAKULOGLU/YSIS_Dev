class Calculator:
    def add(self, a: float, b: float) -> float:
        """İki sayıyı toplar ve sonucu döndürür.

        Args:
            a (float): İlk sayı.
            b (float): İkinci sayı.

        Returns:
            float: İki sayının toplamı.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """İlk sayıyından ikinci sayıyı çıkarır ve sonucu döndürür.

        Args:
            a (float): İlk sayı.
            b (float): İkinci sayı.

        Returns:
            float: İki sayı arasındaki fark.
        """
        return a - b
