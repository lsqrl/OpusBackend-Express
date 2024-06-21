from datetime import datetime, timezone

class Currency(Base):
    __tablename__ = 'example'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(8), nullable=False)

    def __repr__(self):
        return f"<Currency(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}')>"

class LiquidityPool(Base):
    __tablename__ = 'liquidity_pool'
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_id = Column(String(100), nullable=False)
    balance = Column(Float, nullable=False)

    def __repr__(self):
        return f"<LiquidityPool(id={self.id}, currency_id='{self.currency_id}', balance={self.balance})>"


class LiquidityPoolTrans(Base):
    __tablename__ = 'liquidity_pool_trans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.UTC), nullable=False)
    user_id = Column(String(100), nullable=False)
    pool_id = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<LiquidityPoolTrans(id={self.id}, timestamp='{self.timestamp}', "
                f"user_id='{self.user_id}', pool_id='{self.pool_id}', amount={self.amount})>")


class MarginAccount(Base):
    __tablename__ = 'margin_account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp_opening = Column(DateTime, default=datetime.now(timezone.UTC), nullable=False)
    user_id = Column(String(100), nullable=False)

    def __repr__(self):
        return (f"<MarginAccount(id={self.id}, timestamp_opening='{self.timestamp_opening}', "
                f"user_id='{self.user_id}')>")

class MarginAccountTrans(Base):
    __tablename__ = 'margin_account_trans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.UTC), nullable=False)
    user_id = Column(String(100), nullable=False)
    margin_account_id = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<MarginAccountTrans(id={self.id}, timestamp='{self.timestamp}', "
                f"user_id='{self.user_id}', margin_account_id='{self.margin_account_id}', amount={self.amount})>")

class Option(Base):
    __tablename__ = 'option'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(100), nullable=False)
    maturity = Column(DateTime, nullable=False)
    strike = Column(Float, nullable=False)
    direction = Column(String(4), nullable=False)  # "buy" or "sell"
    type = Column(String(4), nullable=False)       # "call" or "put"
    premium = Column(Float, nullable=False)
    margin = Column(Float, nullable=False)
    notional = Column(Float, nullable=False)

    def __repr__(self):
        return (f"<Option(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}', maturity='{self.maturity}', "
                f"strike={self.strike}, direction='{self.direction}', type='{self.type}', premium={self.premium}, "
                f"margin={self.margin}, notional={self.notional})>")

class TradeLog(Base):
    __tablename__ = 'trade_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.UTC), nullable=False)
    option_id = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=False)

    def __repr__(self):
        return (f"<TradeLog(id={self.id}, timestamp='{self.timestamp}', "
                f"option_id='{self.option_id}', user_id='{self.user_id}')>")                