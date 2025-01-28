from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(
                    "{col_name}={col_value}".format(
                        col_name=col, col_value=getattr(self, col)
                    )
                )

        return "<{class_name}(cols)>".format(
            class_name=self.__class__.__name__,
            cols=cols,
        )
