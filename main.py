
using UnityEngine;

public class PlayerMasterController : MonoBehaviour
{
    [Header("Movement Settings")]
    public CharacterController controller;
    public Transform cameraTransform;
    public float speed = 12f;
    public float gravity = -19.62f;
    public float jumpHeight = 3f;
    
    private Vector3 velocity;
    private bool isGrounded;
    public Transform groundCheck;
    public float groundDistance = 0.4f;
    public LayerMask groundMask;

    [Header("Camera Look Settings")]
    private float xRotation = 0f;
    public float mouseSensitivity = 100f;

    [Header("Gun & Shooting Settings")]
    public float damage = 25f;
    public float range = 100f;
    public float fireRate = 10f;
    private float nextTimeToFire = 0f;
    public ParticleSystem muzzleFlash;
    public GameObject impactEffect;

    void Start()
    {
        // गेम शुरू होते ही माउस कर्सर स्क्रीन के बीच में लॉक हो जाएगा
        Cursor.lockState = CursorLockMode.Locked;
    }

    void Update()
    {
        // 1. माउस से 3D कैमरा घुमाना (Look Around)
        float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity * Time.deltaTime;
        float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity * Time.deltaTime;

        xRotation -= mouseY;
        xRotation = Mathf.Clamp(xRotation, -90f, 90f);

        cameraTransform.localRotation = Quaternion.Euler(xRotation, 0f, 0f);
        transform.Rotate(Vector3.up * mouseX);

        // 2. ज़मीन की जाँच (Ground Check)
        isGrounded = Physics.CheckSphere(groundCheck.position, groundDistance, groundMask);

        if (isGrounded && velocity.y < 0)
        {
            velocity.y = -2f;
        }

        // 3. चलना और दौड़ना (WASD Movement)
        float x = Input.GetAxis("Horizontal");
        float z = Input.GetAxis("Vertical");

        Vector3 move = transform.right * x + transform.forward * z;
        controller.Move(move * speed * Time.deltaTime);

        // 4. जंप करना (Spacebar)
        if (Input.GetButtonDown("Jump") && isGrounded)
        {
            velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
        }

        // ग्रेविटी (Gravity) लागू करना
        velocity.y += gravity * Time.deltaTime;
        controller.Move(velocity * Time.deltaTime);

        // 5. गन शूटिंग (Mouse Click / Fire)
        if (Input.GetButton("Fire1") && Time.time >= nextTimeToFire)
        {
            nextTimeToFire = Time.time + 1f / fireRate;
            Shoot();
        }
    }

    void Shoot()
    {
        if (muzzleFlash != null) muzzleFlash.Play();

        RaycastHit hit;
        // कैमरे की सीध में गोली की दिशा (Raycast) छोड़ना
        if (Physics.Raycast(cameraTransform.position, cameraTransform.forward, out hit, range))
        {
            Debug.Log("निशाने पर लगा: " + hit.transform.name);

            // अगर सामने दुश्मन (Enemy) है तो उसे डैमेज देना
            EnemyAI enemy = hit.transform.GetComponent<EnemyAI>();
            if (enemy != null)
            {
                enemy.TakeDamage(damage);
            }

            // जहाँ गोली टकराई वहाँ इफ़ेक्ट दिखाना
            if (impactEffect != null)
            {
                GameObject impactGO = Instantiate(impactEffect, hit.point, Quaternion.LookRotation(hit.normal));
                Destroy(impactGO, 2f);
            }
        }
    }
}

// दुश्मनों (Bots/Enemies) के लिए छोटा सा हेल्पर कोड
public class EnemyAI : MonoBehaviour
{
    public float health = 100f;

    public void TakeDamage(float amount)
    {
        health -= amount;
        if (health <= 0f)
        {
            Die();
        }
    }

    void Die()
    {
        Destroy(gameObject); // दुश्मन खत्म होने पर गायब हो जाएगा
    }
}
