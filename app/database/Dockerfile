FROM postgres:15

# Set environment variables
ENV POSTGRES_DB=deep_picker_db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password

# Create the database directory and set permissions
RUN mkdir -p /var/lib/postgresql/data && \
    chown -R postgres:postgres /var/lib/postgresql/data && \
    chmod 700 /var/lib/postgresql/data

# Switch to postgres user for security
USER postgres

# Expose the PostgreSQL port
EXPOSE 5432

# Use the default postgres entrypoint
CMD ["postgres"] 